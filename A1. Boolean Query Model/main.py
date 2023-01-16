import os 
import argparse

from utils.utils import getDocs, printDoc
from utils.preprocess import getCleanDocs, lemmatization, tokenize, removeStopWords, removePunctuation, stemming, lemmatization

from lib.wildcard_search import processWildCardSearch, buildQuery 
from lib.zone_index import createZoneIndex, printZoneIndex
from lib.model import BooleanModel

from lib.constants import (
    PATH_DATASET
)

def normalBuild(args):
    docs, doc_paths = getDocs(PATH_DATASET)
    clean_docs = getCleanDocs(docs, normalization_type=args.norm)
    zone_index = createZoneIndex(clean_docs)
    model = BooleanModel(corpus_size=len(clean_docs), inverted_index=zone_index, norm_type=args.norm)
    result = model.process_query(args.query)

    for zone in result.keys():
        print("{zone:<20}{list:<10}".format(zone=zone, list=str(sorted(result[zone]))))
    
    result_docIDs = list(set(result["title"]) | set(result["meta"]) | set(result["characters"]) | set(result["body"]))

    print("\n FILES - ")
    print("{docID:<15}{path:<15}".format(docID="docIDs", path="File Paths"))
    for docID in sorted(result_docIDs):
        print("{docID:<15}{doc_path:<15}".format(docID=docID, doc_path=doc_paths[docID]))

    return result

def indexBuild(args):
    docs, doc_paths = getDocs(PATH_DATASET)
    clean_docs = getCleanDocs(docs)
    zone_index = createZoneIndex(clean_docs)

    printZoneIndex(zone_index, upto=args.upto)
    return zone_index 

def stopWordsBuild(args):
    docs, doc_paths = getDocs(PATH_DATASET)
    clean_docs = getCleanDocs(docs, normalization_type=None)
    
    if args.file == None:
        print(clean_docs)
    else:
        docID = doc_paths.index(args.file)
        printDoc(clean_docs[docID])

    return clean_docs 

def stemBuild(args):
    docs, doc_paths = getDocs(PATH_DATASET)
    clean_docs = getCleanDocs(docs, normalization_type="stemming")
    
    if args.file == None:
        print(clean_docs)
    else:
        docID = doc_paths.index(args.file)
        printDoc(clean_docs[docID])

    return docs 

def lemBuild(args):
    docs, doc_paths = getDocs(PATH_DATASET)
    clean_docs = getCleanDocs(docs, normalization_type="lemmatization")

    if args.file == None:
        print(clean_docs)
    else:
        docID = doc_paths.index(args.file)
        printDoc(clean_docs[docID])

    return docs

def wildCardBuild(args):
    docs, doc_paths = getDocs(PATH_DATASET)
    clean_docs = getCleanDocs(docs)
    zone_index = createZoneIndex(clean_docs)
    vocab = list(zone_index.keys())

    possible_words = processWildCardSearch(args.term, keys=vocab)
    query = buildQuery(possible_words)

    print(query)
    model = BooleanModel(corpus_size=len(clean_docs), inverted_index=zone_index, norm_type=args.norm)
    result = model.process_query(query)

    for zone in result.keys():
        print("{zone:<20}{list:<10}".format(zone=zone, list=str(sorted(result[zone]))))
    
    result_docIDs = list(set(result["title"]) | set(result["meta"]) | set(result["characters"]) | set(result["body"]))

    print("\n FILES - ")
    print("{docID:<15}{path:<15}".format(docID="docIDs", path="File Paths"))
    for docID in sorted(result_docIDs):
        print("{docID:<15}{doc_path:<15}".format(docID=docID, doc_path=doc_paths[docID]))

    return result
    

def main(args):
    if args.build == "normal":
        normalBuild(args)
    
    elif args.build == "index":
        indexBuild(args)
    
    elif args.build == "stop_words":
        stopWordsBuild(args)
    
    elif args.build == "stemming":
        stemBuild(args)
    
    elif args.build == "lemmatize":
        lemBuild(args)

    else:
        wildCardBuild(args)



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-b", "--build", choices=["normal", "index", "stop_words", "wildcard", "stemming", "lemmatize"], default="normal", help="Select build option")

    args, rem_args = parser.parse_known_args()

    if args.build == "normal":
        parser.add_argument("-q", "--query", type=str, required=True, help="Enter query")
        parser.add_argument("-norm", type=str, default="stemming", help="stemming or lemmatization")

    elif args.build == "index":
        parser.add_argument("--upto", type=int, default=8, help="Print upto how many tokens?")

    elif args.build == "wildcard":
        parser.add_argument("-t", "--term", type=str, required=True)
        parser.add_argument("-norm", type=str, default="stemming", help="stemming or lemmatization")

    elif args.build != "wildcard":
        parser.add_argument("-f", "--file", type=str, default=None, help="File path")

    parser.parse_args(rem_args, namespace=args)
    
    main(args)


