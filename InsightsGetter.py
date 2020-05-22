import collections
import numpy as np
import matplotlib.pyplot as plt
import nltk
import pandas as pd
from nltk import bigrams

np.random.seed(1235)

def show_frequencies(documents, doc_indices):
    fig, axes = plt.subplots(3, 3)
    count = 0
    for i in range(3):
        for j in range(3):
            counter = collections.Counter(documents.loc[doc_indices[count], "Document"])
            nr_vals_to_show = 10
            if len(counter)<nr_vals_to_show:
                nr_vals_to_show = len(counter)

            objects = counter.most_common(nr_vals_to_show)
            axes[i, j].bar(np.arange(nr_vals_to_show), [obj[1] for obj in objects], align='center', alpha=0.5)
            axes[i, j].set_xticks(np.arange(nr_vals_to_show))
            axes[i, j].set_xticklabels([obj[0] for obj in objects], rotation=90, fontsize=8)
            axes[i, j].set_ylabel('Word freq', fontsize=8)
            axes[i, j].set_title(documents.loc[doc_indices[count], "Topic"])
            count += 1
    plt.tight_layout()
    plt.show()

def show_cooccurences(documents, doc_indices):
    # Create bigrams from all words in corpus
    fig, axes = plt.subplots(3, 3)
    count = 0
    for i in range(3):
        for j in range(3):
            bi_grams = list(bigrams(documents.loc[doc_indices[count], "Document"]))
            nr_vals_to_show = 10
            if len(bi_grams) < nr_vals_to_show:
                nr_vals_to_show = len(bi_grams)

            bigram_freq = nltk.FreqDist(bi_grams).most_common(nr_vals_to_show)
            axes[i, j].bar(np.arange(nr_vals_to_show), [obj[1] for obj in bigram_freq], align='center', alpha=0.5)
            axes[i, j].set_xticks(np.arange(nr_vals_to_show))
            axes[i, j].set_xticklabels([obj[0][0]+"-"+obj[0][1] for obj in bigram_freq], rotation=90, fontsize=6)
            axes[i, j].set_ylabel('Word freq', fontsize=8)
            axes[i, j].set_title(documents.loc[doc_indices[count], "Topic"])
            count += 1
    plt.tight_layout()
    plt.show()

def show_nr_docs_per_class(documents, nr_individual):
    series = documents["Topic"].value_counts()
    series_first_ones = series[:nr_individual]
    other = series[nr_individual:].sum()
    fig,ax = plt.subplots()
    ax.bar(np.arange(len(series_first_ones)+1), np.append(series_first_ones.values,other))
    ax.set_xticks(np.arange(len(series_first_ones)+1))
    labels = np.append(series_first_ones.index,"other")
    ax.set_xticklabels(labels, rotation=90)
    ax.set_title("Number of documents per class")
    plt.tight_layout()
    plt.show()

def show_document_length(documents):
    fig, ax = plt.subplots()
    ax.grid()
    x =  documents["Document"].apply(lambda x: len(x)).values
    nr_bins = 30
    n, bins, patches = ax.hist(x, nr_bins, facecolor='g', alpha=0.75)
    ax.set_title("Word count in the documents")
    ax.set_xlabel("Number of words")
    ax.set_ylabel("Number of documents in the bin")
    plt.show()

def plot_statistics(documents):
    #For 9 random documents
    doc_indices = np.random.choice(range(len(documents.index)), 9)
    show_frequencies(documents, doc_indices)
    show_cooccurences(documents, doc_indices)
    show_document_length(documents)

    #Per class
    show_nr_docs_per_class(documents, 10)
    nine_most_freq_classes = documents["Topic"].value_counts()[:9].index
    documents =documents[documents['Topic'].isin(nine_most_freq_classes)]
    grouped = documents.groupby("Topic").sum().reset_index()
    show_frequencies(grouped, np.arange(9))
    show_cooccurences(grouped, np.arange(9))

    #We would also plot other infos is we would parse more information from documents


