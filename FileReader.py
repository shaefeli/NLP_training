import re
import xml

import xml.dom.minidom as minidom

def clean_document(path):
    filepath = "corrected_file.sgm"
    with open(path) as f:
        lines = f.readlines()
    corrected = [re.sub(r'&#\d+;', '', file) for file in lines]
    f = open(filepath,"w+")
    f.write("".join(corrected))
    f.close()
    return filepath

def preprocess_document(document):
    return document

def read_documents(path):
    #We use only the economic topics, and only use the first label
    #We also only use the raw document (no date or title or whatever)
    #new_path = clean_document(path)
    dataset = dict()
    new_path = "corrected_file.sgm"
    root = minidom.parse(new_path)
    xml_docs = root.getElementsByTagName("REUTERS")
    for doc in xml_docs:
        for child in doc.childNodes:
            topic = -1
            document = ""
            if child.nodeType == xml.dom.Node.ELEMENT_NODE:
                if child.tagName == 'TOPICS' and child.childNodes:
                    for subchild in child.childNodes:
                        if subchild.nodeType == xml.dom.Node.ELEMENT_NODE and subchild.tagName=="D":
                            topic = subchild.childNodes[0].nodeValue
                if child.tagName == "TEXT":
                    for subchild in child.childNodes:
                        if subchild.nodeType == xml.dom.Node.ELEMENT_NODE and subchild.tagName=="BODY":
                            document = subchild.childNodes[0].nodeValue

            if topic !=-1:
                document = preprocess_document(document)
                if topic in dataset:
                    dataset[topic].append(document)
                else:
                    dataset[topic] = [document]

    return dataset




