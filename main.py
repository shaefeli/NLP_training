from tdidf import *
from FileReader import *
documents = read_documents("reut2-000.sgm")
#For the moment, we use everything as a train dataset
td_idf_embeddings = td_idf(documents)