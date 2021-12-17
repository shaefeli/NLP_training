## Goal
This repository contains some basic implementations for NLP document classification. 
It also contains a file used to implement Regex basics

## Dataset 
We use the Reuters Dataset. We extract the text document and the economic topic, aim of the classification. 
Since the document distribution per class varies a lot, we sometimes only keep the 10 most frequent classes. 

## Implementation
Following is implemented: 
#### Data gathering: 
-Parse the data from raw xml files to pandas series. Clean the data to make it readable
#### Text preprocessing:
-Lowercase
-Remove punctuation
-Remove stopwords
-Replace numbers
-Tokenization (1gram)
#### Statistics:
-show most frequent words, bigrams, word count, for random documents and per class
#### Classification:
-Use the td/idf vectorization (three different variants implemented) and the multinomial logisitc regression

## Current results:
Using 90% of the dataset for training (~9000 documents) and 10% for testing. 
=>Achieves 75% test accuracy
Using only the 10 most frequent classes (~8000 documents), splitting again by using 90% for training.
=>Achieves 93% test accuracy


## To come: 
-More preprocessing (POS Tagger, stemming, Entity name recognition)  
-Implement word embeddings (word2vec and FastText)  
-Use more complicated models (LSTMs, and XGBoost models)  
-Find a solution regarding the document count per class   
