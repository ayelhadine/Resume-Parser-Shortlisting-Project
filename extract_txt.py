from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import mammoth
import textract
import os
import io


def extract_text_from_pdf(pdf_path):
    """
    This function returns a text from pdf file
    :param pdf_path: path for the pdf file
    :return: text
    """
    r_manager = PDFResourceManager()
    output = io.StringIO()
    converter = TextConverter(r_manager, output, laparams=LAParams())
    p_interpreter = PDFPageInterpreter(r_manager, converter)

    with open(pdf_path, 'rb') as file:
        for page in PDFPage.get_pages(file, caching=True, check_extractable=True):
            p_interpreter.process_page(page)
            text = output.getvalue()
        
    converter.close()
    output.close()

    return text


 
def extract_text_from_docx(docx_path):
    """
    This function returns a text from a docx file
    :param docx_path: path for the docx file
    :return:text
    """
    with open(docx_path, 'rb') as docx_file:
        result = mammoth.extract_raw_text(docx_file)
        text = result.value
    
    return text

 
def read_files(file_path):
    """
    This function returns a list of texts from multiples files
    :param file_path: path for the directory that contains multiples pdf, docx and doc files
    :return: returns list of texts
    """
    fileTXT=[]

    for filename in os.listdir(file_path):
        if filename.endswith(".pdf"):
            try:
                fileTXT.append(extract_text_from_pdf(file_path+filename))
            except Exception:
                print("Error Reading pdf file :" + filename)
        
        if filename.endswith(".docx"):
            try:
                fileTXT.append(extract_text_from_docx(file_path+filename))
            except Exception:
                print("Error reading docx file:" + filename)

        if filename.endswith(".doc"):
            try:
                fileTXT.append(textract.process(file_path+filename).decode('utf-8'))
            
            except Exception:
                print('Error reading .doc file :' + filename)
    
    return fileTXT


if __name__=="__main__":
    txt = read_files("/home/ayoub/DS/Parser-Shortlisting-Project/files/resumes")
    print(txt)