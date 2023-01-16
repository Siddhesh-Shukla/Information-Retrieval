import os

# docs = {
#     0: {
#         "title": "string",
#         "meta": "", 
#         "characters": "", 
#         "body": ""
#     } 
# }

def getFileNames(path_dataset):
    """
        Returns list of file-names

        Parameters:
        path_dataset: Path to dataset
    """
    return os.listdir(path_dataset)

def getDoc(file_path):
    """
        Get zone wise doc content

        Parameters:
        file_path: path to a certain document

        Returns: 
        document separated into 4 zones - title, meta, characters, body
    """

    content = ""
    with open(file_path, 'r') as file:
        for line in file:
            content += line 

    content = content.split("\n")

    title = content[0]

    content[1:8].remove("")
    meta = " ".join(content[1:8])

    characters = ""
    body = ""

    if "Characters in the Play" in content[7:]:
        idx = content.index("Characters in the Play")
        content = content[idx:]
    else:
        content[8:].remove("")
        body = " ".join(content[8:])

    body_zone_idx = content.index("")
    if "" in content[:body_zone_idx]:
        content[:body_zone_idx].remove("")
    characters = " ".join(content[:body_zone_idx])

    body_zone = content[body_zone_idx:]
    if "" in body_zone:
        body_zone.remove("")
    body = " ".join(body_zone)

    doc = {
        "title": title, 
        "meta": meta,
        "characters": characters, 
        "body": body
    }

    return doc 

def getDocs(path_dataset):
    """
    Returns a dictionary with docID keys and docContent segregated into zones 

    Parameters:
    path_dataset: Path to dataset 
    """

    docs = {}
    doc_paths = []

    files = getFileNames(path_dataset)
    docID = 0
    for file in files:
        file_path = f"{path_dataset}/{file}"
        doc_paths.append(file_path)

        doc = getDoc(file_path)

        docs.update({docID: doc})
        docID += 1

    return docs, doc_paths


def getResultFilePaths(result, zone, doc_paths):
    """
        get file paths for query results
    """
    result_paths = []

    for docID in result[zone]:
        result_paths.append(doc_paths[docID])
    
    return result_paths


# Args utils

def printDoc(doc):
    for zone in doc.keys():
        print("{zone:<15}{list:<10}".format(zone=zone, list=str(doc[zone])))
        print("\n\n")
        

