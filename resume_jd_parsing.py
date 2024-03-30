import logging
import re
import csv
import spacy
from spacy.matcher import Matcher
from pdfminer.high_level import extract_text
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeExtractor:
    def __init__(self, skills_list: list = None):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = Matcher(self.nlp.vocab)
        self.skills_list = skills_list or []

        # Define name patterns
        self.patterns = [
            [{"POS": "PROPN"}, {"POS": "PROPN"}],
            [{"POS": "PROPN"}, {"POS": "PROPN"}, {"POS": "PROPN"}],
            [{"POS": "PROPN"}, {"POS": "PROPN"}, {"POS": "PROPN"}, {"POS": "PROPN"}],
        ]
        for pattern in self.patterns:
            self.matcher.add("NAME", patterns=[pattern])

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text from a PDF file.
        """
        return extract_text(str(pdf_path))

    def extract_contact_number(self, text):
        pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
        match = re.search(pattern, text)
        return match.group() if match else None

    def extract_email(self, text):
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        match = re.search(pattern, text)
        return match.group() if match else None

    def extract_skills(self, text: str) -> list:
        """
        Extract skills from the given text.
        """
        # Preprocess text: convert to lowercase and remove punctuation
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        
        # Extract skills using predefined list and remove duplicates
        skills = list(set(skill for skill in self.skills_list if skill.lower() in text))
        return skills

    def extract_education(self, text: str) -> list:
        """
        Extract education from the given text.
        """
        pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"
        return re.findall(pattern, text, re.IGNORECASE)

    def extract_name(self, text: str) -> str:
        """
        Extract name from the given text.
        """
        doc = self.nlp(text)
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            return span.text
        return None

    def extract_skills_from_jd(self, jd_text: str) -> list:
        """
        Extract skills from the given JD text.
        """
        # Preprocess JD text: convert to lowercase and remove punctuation
        jd_text = jd_text.lower()
        jd_text = re.sub(r'[^\w\s]', '', jd_text)
        
        # Extract skills using predefined list and remove duplicates
        jd_skills = list(set(skill for skill in self.skills_list if skill.lower() in jd_text))
        return jd_skills

    def check_skills_with_jd(self, resume_skills: list, jd_skills: list) -> float:
        """
        Calculate the cosine similarity between the resume skills and JD skills.
        """
        if not resume_skills or not jd_skills:
            return 0

        vectorizer = TfidfVectorizer(min_df=1)
        resume_skills = [skill for skill in resume_skills if skill]  # Remove empty strings
        resume_skills_vector = vectorizer.fit_transform(resume_skills)
        jd_skills_vector = vectorizer.transform(jd_skills)

        return (resume_skills_vector * jd_skills_vector.T).sum() / (
            np.sqrt((resume_skills_vector * resume_skills_vector.T).sum()) * 
            np.sqrt((jd_skills_vector * jd_skills_vector.T).sum())
        )

    def process_jd_and_resume_in_directory(self, jd_directory, resume_directory, output_file, jd_text_file):
        """
        Process JDs and resumes in the given directories and save the result to the given output file.
        """
        # Load the JD text
        with open(jd_text_file, 'r', encoding='utf-8') as file:
            jd_text = file.read()

        # Extract resumes and skills
        pdf_files = list(resume_directory.glob("*.pdf"))
        results = []
        for pdf_path in pdf_files:
            text = self.extract_text_from_pdf(pdf_path)
            name = self.extract_name(text)
            contact_number = self.extract_contact_number(text)
            email = self.extract_email(text)
            skills = self.extract_skills(text)
            education = self.extract_education(text)

            jd_skills = self.extract_skills_from_jd(jd_text)
            similarity = self.check_skills_with_jd(skills, jd_skills)

            results.append({
                "Resume": pdf_path.name,
                "Name": name,
                "Contact Number": contact_number,
                "Email": email,
                "Skills": [{"Skill": skill} for skill in skills],
                "Education": [{"Education": edu} for edu in education],
                'JD Skills': jd_skills,
                'Similarity': similarity
            })

        # Save results to CSV
        with open(output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

        logger.info(f"Results saved to {output_file}")

if __name__ == "__main__":
    # Specify the directory containing the JDs and resumes
    jd_directory = Path(r"C:\Users\Shami\Documents\MSc AI\Sem1 - Data Analytics\Project\Resume_rank\data\job_descriptions")
    resume_directory = Path(r"C:\Users\Shami\Documents\MSc AI\Sem1 - Data Analytics\Project\Resume_rank\data\resumes")

    # Specify the output file
    output_file = Path("jd_and_resume_data.csv")

    # Specify the JD text file
    jd_text_file = Path("job_descriptions.txt")

    # Read the skills list from a CSV file
    skills_file = Path(r"C:\Users\Shami\Documents\MSc AI\Sem1 - Data Analytics\Project\Resume_rank\data\skills\skill_red.csv")
    with open(skills_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        skills_list = [row[0].strip() for row in reader]

    # Create ResumeExtractor instance
    extractor = ResumeExtractor(skills_list)

    # Process JDs and resumes in the specified directories and save results
    extractor.process_jd_and_resume_in_directory(jd_directory, resume_directory, output_file, jd_text_file)
