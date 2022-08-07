import re
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords

def preprocess(txt):
    """
    This function returns a preprocessed list of texts 
    :param txt: list containing texts
    :return: preprocessed list of texts
    """
    sw = stopwords.words('english')
    space_pattern = '\s+'
    special_letters =  "[^a-zA-Z#]]"
    p_txt = []

    for resume in txt : 
        text = re.sub(space_pattern, ' ', resume)# remove extra spaces
        text = re.sub(special_letters, ' ', text)#remove special characteres
        text = re.sub(r'[^\w\s]', '',text)#remove punctuations
        text = text.split() #split words in a text
        text = [word for word in text if word.isalpha()] #keep alphabetic word
        text = [w for w in text if w not in sw] #remove stop words
        text = [item.lower() for item in text] #lowercase words
        p_txt.append(" ".join(text))#joins all words

    return p_txt
