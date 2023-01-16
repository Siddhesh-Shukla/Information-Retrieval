import re 
from nltk.corpus import stopwords, words  
from nltk.stem import PorterStemmer, WordNetLemmatizer

from nltk.tokenize import word_tokenize
from nltk.metrics.distance import edit_distance

# Stop words 
STOP_WORDS = stopwords.words('english')
CORRECT_WORDS = words.words()

porter = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# docs = {
#   docID: {
#        "zone-1": ["token-1", "token-2", ...] 
#        "zone-2": ["token-1", "token-2", ...]
#        "zone-3": ["token-1", "token-2", ...]
#   }
# }


def lowerCaseText(docContent: dict, zones=["title", "meta", "characters", "body"]) -> dict:
    """
        Returns lowercased text

        Parameters:
        docContent: contents of documents separated in zones
        zones: List of zones in which we use this preprocessing method
    """

    for zone in zones:
        docContent[zone] = docContent[zone].lower()

    return docContent
    

def tokenize(docContent: dict) -> dict:
    """
        Returns list of tokens 

        Parameters:
        docContent: contents of documents separated in zones
    """

    docContent["title"] = word_tokenize(docContent["title"])

    docContent["meta"] = word_tokenize(docContent["meta"])

    docContent["characters"] = word_tokenize(docContent["characters"])

    docContent["body"] = word_tokenize(docContent["body"])
    return docContent

def removeStopWords(docContent: dict, zones=["title", "meta", "characters", "body"], stop_words=STOP_WORDS) -> dict:
    """
        Returns the filtered tokens

        Parameters:
        docContent: contents of documents separated in zones
        zones: List of zones in which we use this preprocessing method
        stop_words: List of stopwords 
    """ 

    for zone in zones:
        docContent[zone] = [token for token in docContent[zone] if token not in stop_words]

    return docContent

def removePunctuation(docContent, zones=["title", "meta", "characters", "body"], punctuations="!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~="):
    """
        Returns tokens after removing punctuations

        Parameters:
        docContent: contents of documents separated in zones
        zones: List of zones in which we use this preprocessing method
        punctuations: List of characters which we dont want to consider 
    """

    for zone in zones:
        docContent[zone] = re.sub('[%s]' % re.escape(punctuations), ' ', docContent[zone])

    return docContent


def stemming(docContent, zones=["title", "meta", "characters", "body"]):
    """
        Returns the stemmed version of tokens

        Parameters:
        docContent: contents of documents separated in zones
        zones: List of zones in which we use this preprocessing method
    """

    for zone in zones:
        docContent[zone] = [porter.stem(token) for token in docContent[zone]]
    
    return docContent

def lemmatization(docContent, zones=["title", "meta", "characters", "body"]):
    """
        Returns lemmatized version of tokens

        Parameters:
        docContent: contents of documents separated in zones
        zones: List of zones in which we use this preprocessing method
    """
    for zone in zones:
        docContent[zone] = [lemmatizer.lemmatize(token) for token in docContent[zone]]

    return docContent

def getCleanDocs(docs, remove_stopwords=True, remove_puncuation=True, normalization_type="stemming"):
    """
        Pipelined preprocessing

        Parameters:
        docs: dictionary of docs 
        remove_stopwords: if true removes stop_words 
        remove_puncutation: if true removes puncuation 
        normalization_type: if "stemming" will stem the tokens else if "lemmatization" will lemmatize the tokens

        Returns:
        clean_docs: Clean preprocessed documents in dictionary format
    """

    if remove_puncuation:
        for docID, docContent in docs.items():
            docs[docID] = removePunctuation(docContent)

    for docID, docContent in docs.items():
        docs[docID] = lowerCaseText(docContent)
        docs[docID] = tokenize(docContent)

    if remove_stopwords:
        for docID, docContent in docs.items():
            docs[docID] = removeStopWords(docContent)

    if normalization_type == "stemming":
        for docID, docContent in docs.items():
            docs[docID] = stemming(docContent)
    
    elif normalization_type == "lemmatization":
        for docID, docContent in docs.items():
            docs[docID] = lemmatization(docContent)
        
    
    for docID, docContent in docs.items():
        if "" in docContent["title"]:
            docContent["title"].remove("")
        
        if "" in docContent["meta"]:
            docContent["meta"].remove("")
        
        if "" in docContent["characters"]:
            docContent["characters"].remove("")

        if "" in docContent["body"]:
            docContent["body"].remove("")

    return docs


def correctSpelling(token):
    """
        Spelling correction using Edit Distance method

        Parameter: 
        token: Token in query
    """

    possible_words = [(edit_distance(token, w), w) for w in CORRECT_WORDS if w[0] == token[0]]
    correct_token = sorted(possible_words, key = lambda val: val[0])[0][1] 
    return correct_token

def getCleanQueryToken(token, normalization_type="stemming", spelling_correction=True):
    """
        Preprocesses the token present in the query 

        Parameters:
        token: token in query
        normalization_type: if "stemming" will stem the token else if "lemmatization" will lemmatize the token
    """
    
    token = token.lower()
    
    # TODO -> spelling correction
    if spelling_correction:
        token = correctSpelling(token) 

    if normalization_type == "stemming":
        token = porter.stem(token)
    
    elif normalization_type == "lemmatization":
        token = lemmatizer.lemmatize(token)

    return token

