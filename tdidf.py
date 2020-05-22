import collections
import numpy as np
import sys
import math
import time
import pickle
import csv

def td_idf(documents, vocabulary ,method=2, ngrams=1, from_memory=False, train=True, writeSomeToCSV=False):
    "Reflects how important a word is to a document in a collection"
    "A survey conducted in 2015 showed that 83% of text-based recommender systems in digital libraries use tf–idf"
    "https://en.wikipedia.org/wiki/Tf–idf"
    "Method refers to the method number presented in the wikipedia page"
    "n-grams represents the number of contigous word used to do tf-idf. Only ngrams=1 is implemented for the moment"

    if from_memory:
        if train:
            with open("Saver/td_idf_mat_train", "rb") as fp:
                td_idf_matrix = pickle.load(fp)
        else:
            with open("Saver/td_idf_mat_test", "rb") as fp:
                td_idf_matrix = pickle.load(fp)

    else:

        td_idf_matrix = np.zeros((len(documents.index), len(vocabulary)))

        start_td_idf = time.time()
        # Compute the td in pandas
        if method == 1:
            td = documents["Document"].apply(lambda doc: [vocabulary.index(word) for word in doc if word in vocabulary])
        elif method == 2:
            td = documents["Document"].apply(lambda doc: {k: v * 1.0 / len(doc) for k, v in dict(
                collections.Counter([vocabulary.index(word) for word in doc if word in vocabulary])).items()})
        elif method == 3:
            td = documents["Document"].apply(lambda doc: {k: math.log(1 + v) for k, v in dict(
                collections.Counter([vocabulary.index(word) for word in doc if word in vocabulary])).items()})

        computing_td = time.time()
        print("Time to compute td:", computing_td - start_td_idf, "seconds")

        idf = np.empty(len(vocabulary))
        N = len(documents.index)
        idf = list(
            map(lambda term: math.log(N / 1+ documents["Document"].apply(lambda doc: 1 if term in doc else 0).sum()),
                vocabulary))

        calculating_idf = time.time()
        print("Time to calculate idf:", calculating_idf - computing_td, "seconds")

        # Fill the td/idf matrix with the td and idf values
        for i, doc in enumerate(td):
            for (k, v) in doc.items():
                td_idf_matrix[i, k] = v * idf[k]

        filling = time.time()
        print("Time to fill in td/idf in the matrix:", filling - calculating_idf, "seconds")

        if train:
            with open("Saver/td_idf_mat_train", "wb") as fp:
                pickle.dump(td_idf_matrix, fp)
        else:
            with open("Saver/td_idf_mat_test", "wb") as fp:
                pickle.dump(td_idf_matrix, fp)

    if writeSomeToCSV:
        with open("Saver/some_td_idf_embeddings.csv", 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(documents["Topic"][:100])
            wr.writerow(td_idf_matrix[:100, 0])
            wr.writerow(td_idf_matrix[:100, 1])
            wr.writerow(td_idf_matrix[:100, 4])
            wr.writerow(td_idf_matrix[:100, 175])
            wr.writerow(td_idf_matrix[:100, 17])
            wr.writerow(td_idf_matrix[:100, 127])
            wr.writerow(td_idf_matrix[:100, 5])

    return td_idf_matrix

def get_vocabulary(documents, max_length=5000):
    vocab = list()
    documents["Document"].apply(lambda x: vocab.extend(x))
    counter = collections.Counter(vocab).most_common(max_length)
    return [x[0] for x in counter]