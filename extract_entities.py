import re
from nltk import sent_tokenize, pos_tag, word_tokenize, everygrams
from nltk.corpus import wordnet, stopwords

def get_number(text):
    """
    This function returns a list of a phone number from a list of text
    :param text: list of text
    :return: list of a phone number
    """
    # compile helps us to define a pattern for matching it in the text
    pattern = re.compile(r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
    # findall finds the pattern defined in compile
    pt = pattern.findall(text)

    # sub replaces a pattern matching in the text
    pt = [re.sub(r'[,.]', '', ah) for ah in pt if len(re.sub(r'[()\-.,\s+]', '', ah))>9]
    pt = [re.sub(r'\D$', '', ah).strip() for ah in pt]
    pt = [ah for ah in pt if len(re.sub(r'\D','',ah)) <= 15]

    for ah in list(pt):
        # split splits a text
        if len(ah.split('-')) > 3: continue
        for x in ah.split("-"):
            try:
                # isdigit checks whether the text is number or not
                if x.strip()[-4:].isdigit():
                    if int(x.strip()[-4:]) in range(1900, 2100):
                        pt.remove(ah)
                    
            except: pass

        number = None
        number = list(set(pt))
        return number



def get_email(text):
    """
    This function returns a list of an email from a list of text
    :param text: list of text
    :return: list of an email
    """
    # compile helps us to define a pattern for matching it in the text
    r = re.compile(r'[A-Za-z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    return r.findall(str(text))



def rm_number(text):
    """
    This function removes phone number from a list of text
    :param text: list of text
    :return: list of text without phone number
    """
    try:
        # compile helps us to define a pattern for matching it in the text
        pattern = re.compile(r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
        # findall finds the pattern defined in compile
        pt = pattern.findall(text)
        # sub replaces a pattern matching in the text
        pt = [re.sub(r'[,.]', '', ah) for ah in pt if len(re.sub(r'[()\-.,\s+]', '', ah))>9]
        pt = [re.sub(r'\D$', '', ah).strip() for ah in pt]
        pt = [ah for ah in pt if len(re.sub(r'\D','',ah)) <= 15]
        for ah in list(pt):
            if len(ah.split('-')) > 3: continue
            for x in ah.split("-"):
                try:
                    # isdigit checks whether the text is number or not
                    if x.strip()[-4:].isdigit():
                        if int(x.strip()[-4:]) in range(1900, 2100):
                    # removes a the mentioned text
                            pt.remove(ah)
                except: pass

        number = None
        number = pt
        number = set(number)
        number = list(number)
        for i in number:
            text = text.replace(i," ")
        return text
        
    except: pass


def rm_email(text):
    """
    This function removes email from a list of text
    :param text: list of text
    :return: list of text without email
    """
    try:
        email = None
        # compile helps us to define a pattern for matching it in the text
        pattern = re.compile('[\w\.-]+@[\w\.-]+')
        # findall finds the pattern defined in compile
        pt = pattern.findall(text)
        email = pt
        email = set(email)
        email = list(email)
        for i in email:
            # replace will replace a given string with another
            text = text.replace(i," ")

        return text

    except: pass



def get_name(text):
    """
    This function returns a candidate name from a list of text
    :param text: list of text
    :return: string of a candidate name
    """
    # Tokenizes whole text to sentences
    Sentences = sent_tokenize(text)
    t = []

    for s in Sentences:
        # Tokenizes sentences to words
        t.append(word_tokenize(s))
    # Tags a word with its part of speech
    words = [pos_tag(token) for token in t]
    n = []
    for x in words:
        for l in x:
        # match matches the pos tag of a word to a given tag here
            if re.match('[NN.*]', l[1]):
                n.append(l[0])

    cands = []
    for nouns in n:
        if not wordnet.synsets(nouns):
            cands.append(nouns)

    cand = ' '.join(cands[:1])
    return cand



def get_skills(text,skills):
    """
    This function returns a list of skills from a list of text
    :param text: list of text
    :param skills: dataframe of predefined skills
    :return: list of skills
    """
    
    sw = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    # remove the punctuation
    ft = [w for w in tokens if w.isalpha()]
    # remove the stop words
    ft = [w for w in tokens if w not in sw]
    # generate bigrams and trigrams
    n_grams = list(map(' '.join, everygrams(ft, 2, 3)))
    fs = set()
    # we text for each token in our skills database
    for token in ft:
        if token.lower() in skills:
            fs.add(token)
    
    for ngram in n_grams:
        if ngram.lower() in skills:
            fs.add(ngram)
    return fs
