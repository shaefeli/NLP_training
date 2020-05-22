import re
import string
from nltk.corpus import stopwords
import pickle

def preprocess_documents(documents):

    #Put everything to lower case
    print("Documents to lowercase")
    documents["Document"] = documents["Document"].apply(lambda x: x.lower().strip())

    #Remove punctuation
    #No translation here, but quick way to remove punctuation
    print("Remove punctuations")
    documents["Document"] = documents["Document"].apply(lambda s: s.translate(str.maketrans('', '', string.punctuation)))

    #Remove english stopwords
    print("Remove stopwords")
    def remove_words_from_list(s, to_remove_list):
        for word in to_remove_list:
            s = re.sub(r'\b'+word+r'\b',"",s)
        return s
    stop_words = set(stopwords.words('english'))
    documents["Document"] = documents["Document"].apply(lambda s: remove_words_from_list(s,stop_words))


    #Replace numbers by a mark
    #Note that since we removed stopwords like "and", we can have 30 and 40 and 50 ... => 30 40 50 ...
    print("Replace numbers by <NUMBER>")
    documents["Document"] = documents["Document"].apply(lambda x: re.sub(r'(\d+(\s+\d+)*)',"<NUMBER>",x))

    #Replace more than one whitespaces by one
    documents["Document"] = documents["Document"].apply(lambda x: re.sub(r'\s+'," ", x))


    #More steps to come right here!
    #print(documents.loc[0,"Document"])
    print("Tokenizing documents")
    def tokenize(x):
        tokens = x.split(" ")
    documents["Document"] = documents["Document"].apply(lambda x: tokenize(x))

    with open("Reuters_Data/preprocessed", "wb") as fp:
        pickle.dump(documents, fp)

    return documents

