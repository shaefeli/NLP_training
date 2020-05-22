import re
import xml
import xml.dom.minidom as minidom
import pandas as pd
import os

def clean_document(filename, full_path,  corrected_path):
    with open(full_path) as f:
        lines = f.readlines()
    corrected = [re.sub(r'&#\d+;', '', file) for file in lines] #Correct this unreadable character
    corrected.insert(1,"<FILE>")  #Add a top element to the document that we will call <FILE>
    corrected.append("</FILE>")
    stem = re.search(r'(.*).sgm',filename).group(1)
    filepath=os.path.join(corrected_path, stem+"_corrected.sgm")
    f = open(filepath,"w+")
    f.write("".join(corrected))
    f.close()
    return filepath


def read_documents(path, dataset):
    #We use only the economic topics, and only use the first label
    #We also only use the raw document (no date or title or whatever)
    #Note that some documents are filtered out because they contain no text
    root = minidom.parse(path)
    xml_docs = root.getElementsByTagName("REUTERS")
    for doc in xml_docs:
        topic = -1
        document = ""
        for child in doc.childNodes:
            if child.nodeType == xml.dom.Node.ELEMENT_NODE:
                if child.tagName == 'TOPICS' and child.childNodes:
                    for subchild in child.childNodes:
                        if subchild.nodeType == xml.dom.Node.ELEMENT_NODE and subchild.tagName=="D":
                            topic = subchild.childNodes[0].nodeValue
                if child.tagName == "TEXT":
                    for subchild in child.childNodes:
                        if subchild.nodeType == xml.dom.Node.ELEMENT_NODE and subchild.tagName=="BODY":
                            document = subchild.childNodes[0].nodeValue

        if topic !=-1 and document != "":
            dataset = dataset.append({'Topic': topic, 'Document': document}, ignore_index=True)
    return dataset


def clean_all_documents(path, corrected_path):
    for file in os.listdir(path):
        clean_document(file, os.path.join(path, file), corrected_path)

def read_all_documents(path, clean=False):
    corrected_path = "Reuters_data/corrected"
    if clean:
        clean_all_documents(path, corrected_path) #Make them readable by the dom xml parser

    dataset = pd.DataFrame(columns=['Topic', 'Document'])
    for file in os.listdir(corrected_path):
        print("Reading file",file,"into memory...")
        dataset = read_documents(os.path.join(corrected_path, file),dataset)

    print("Loaded",len(dataset.index),"documents in memory")
    return dataset



