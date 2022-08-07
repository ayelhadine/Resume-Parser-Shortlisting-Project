from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def simil(feats, p_resumetxt, p_jdtxt):
    """
    This function returns a dataframe of similiraty scores
    between resumes and job description
    :param p_resumetxt: preprocessed list of resume texts
    :param p_jdtxt: preprocessed list of job description texts
    :param feats: dataframe of text features
    :return: dataframe of similiraty scores 
    """
    similarity = cosine_similarity(feats[0:len(p_resumetxt)],feats[len(p_resumetxt):])
    abc = []
    for i in range(1,len(p_jdtxt)+1):
        abc.append(f"JD {i}")

    # DataFrame of similarity score
    df_sim=pd.DataFrame(similarity,columns=abc)

    return df_sim




