from tdidf import *
from FileReader import *
from DocumentPreprocessing import *
from InsightsGetter import *
from DatasetSplitter import *
from Classifier import *
import pickle

pre_processing_from_memory = True
show_stats = False
training = False
testing = True

if pre_processing_from_memory:
    with open("Reuters_Data/preprocessed", "rb") as fp:
        documents = pickle.load(fp)
else:
    documents = read_all_documents("Reuters_data/original", clean=False)
    documents = preprocess_documents(documents)

if show_stats:
    plot_statistics(documents)

#Get the first 10 most frequent topics
ten_most_freq_topics = list(documents["Topic"].value_counts()[:10].index)
documents = documents[documents.Topic.isin(ten_most_freq_topics)]

train_dataset, test_dataset = split_dataset(documents, ratio=0.9)
vocabulary = get_vocabulary(train_dataset, max_length=5000)

if training:
    td_idf_embeddings_train = td_idf(train_dataset, vocabulary, from_memory=True, train=True, writeSomeToCSV=False) #Returns a matrix of size [nr_documents,vocab_size]
    trained_classifier = log_reg(td_idf_embeddings_train, train_dataset["Topic"])
    with open("Saver/model_classifier", "wb") as fp:
        pickle.dump(trained_classifier, fp)

if testing:
    with open("Saver/model_classifier", "rb") as fp:
        trained_classifier = pickle.load(fp)
    td_idf_embeddings_test = td_idf(test_dataset, vocabulary, from_memory=True, train=False, writeSomeToCSV=False)
    score = trained_classifier.score(td_idf_embeddings_test, test_dataset["Topic"])
    print("Test score: ",score*100,"%")






