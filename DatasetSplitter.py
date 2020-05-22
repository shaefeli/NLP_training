import numpy as np

def split_dataset(documents, ratio=0.8):
    np.random.seed(1234)
    if ratio==1:
        return documents, None
    elif ratio==0:
        return None, documents
    else:
        nr_documents = len(documents.index)
        indices_train = np.random.choice(nr_documents, int(nr_documents*ratio), replace=False)
        indices_test = np.setdiff1d(np.arange(nr_documents), indices_train, assume_unique=True)
        return documents.iloc[indices_train], documents.iloc[indices_test]