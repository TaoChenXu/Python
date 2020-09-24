"""
inverted_index.py

Build a basic (naive) inverted index for a simple (naive) documents set
Please Run this script using Python3.x
Tested under Python3.6, Win7 and Python3.5 ubuntu16.04
Author: Richy Zhu
Email: rickyzhu@foxmail.com
"""

import json
import re
from pprint import pprint


def clear_symbols(text):
    """remove symbols like commas, semi-commas
    """
    simbols = re.compile("[\s+\.\!\/_,$%^*()+\"\']+|[+——！，。？、~@#￥%……&*（）：]+")
    if type(text) is str:
        processed_text = re.sub(simbols, ' ', text)
        return processed_text
    elif type(text) is list:
        return [re.sub(simbols, ' ', item) for item in text]
    else:
        raise TypeError("This function only accept str or list as argument")


def lowercase(text):
    """turn all the characters to be lowercase
    """
    if type(text) is str:
        return text.lower()
    elif type(text) is list:
        return [item.lower() for item in text]
    else:
        raise TypeError("This function only accept str or list as argument")


def tokenize(docs):
    token_stream = []
    for doc in docs:
        token_stream.append(doc.split())
    return token_stream


def preprocess(docs):
    """clear symbols, lowercase, tokenize, get clean tokenized docs
    """
    normalized_docs = lowercase(clear_symbols(docs))
    tokenized_docs = tokenize(normalized_docs)
    return tokenized_docs


def get_token_stream(tokenized_docs, docs_dict):
    """get (term-doc_id) stream
    """
    token_stream = []
    for doc_id in docs_dict:
        for term in tokenized_docs[doc_id]:
            token_stream.append((term, doc_id))
    return token_stream


def build_indices(tokenized_docs, docs_dict):
    """main function -- build invertex index
       assume that the documents set is small enough to be loaded into Memory
    """
    token_stream = get_token_stream(tokenized_docs, docs_dict)
    # pprint(token_stream)
    indices = {}

    for pair in token_stream:
        if pair[0] in indices:
            if pair[1] not in indices[pair[0]]:
                indices[pair[0]].append(pair[1])
        else:
            indices[pair[0]] = [pair[1]]
    return indices


if __name__ == "__main__":
    docs = [
        "hello world",
        "hello python",
        "I love C, Java, Python, Typescript, and PHP",
        "use python to build inverted indices",
        "you and me are in one world"
    ]
    docs_dict = {
        0: "docs[0]",
        1: "docs[1]",
        2: "docs[3]",
        3: "docs[4]",
        4: "docs[5]"
    }
    tokenized_docs = preprocess(docs)
    # pprint(tokenized_docs)
    indices = build_indices(tokenized_docs, docs_dict)
    pprint(indices)






























































































