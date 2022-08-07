from extract_txt import read_files
from txt_processing import preprocess
from txt_to_features import txt_features, feats_reduce
from extract_entities import get_number, get_email, rm_email, rm_number, get_name, get_skills, get_location
from model import simil
import pandas as pd
#import nltk
#nltk.download('omw-1.4')


if __name__=="__main__":
    directory = '/home/ayoub/DS/Parser-Shortlisting-Project/Data/'
    resume_path = '/home/ayoub/DS/Parser-Shortlisting-Project/files/resumes'
    jd_path = directory + 'JobDesc/'

    resumetxt=read_files(resume_path)
    p_resumetxt = preprocess(resumetxt)

    jdtxt=read_files(jd_path)
    p_jdtxt = preprocess(jdtxt)
    
    feats = txt_features(p_resumetxt, p_jdtxt)
    feats_red = feats_reduce(feats)

    df = simil(feats_red, p_resumetxt, p_jdtxt)

    t = pd.DataFrame({'Original Resume':resumetxt})
    dt = pd.concat([df,t],axis=1)
    dt['Phone No.']=dt['Original Resume'].apply(lambda x: get_number(x))
    
    dt['E-Mail ID']=dt['Original Resume'].apply(lambda x: get_email(x))

    dt['Original']=dt['Original Resume'].apply(lambda x: rm_number(x))
    dt['Original']=dt['Original'].apply(lambda x: rm_email(x))
    dt['Candidate\'s Name']=dt['Original'].apply(lambda x: get_name(x))

    skills = pd.read_csv('/home/ayoub/DS/Parser-Shortlisting-Project/Data/skill_red.csv')
    skills = skills.values.flatten().tolist()
    skill = []
    for z in skills:
        r = z.lower()
        skill.append(r)

    dt['Skills']=dt['Original'].apply(lambda x: get_skills(x,skill))
    dt['Location']=dt['Original'].apply(lambda x: get_location(x))
    print(dt['Location'].head(30))

