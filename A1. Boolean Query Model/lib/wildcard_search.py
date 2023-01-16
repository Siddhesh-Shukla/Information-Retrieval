def rotate(str, n):
    """
        Returns one rotation of str
    """

    return str[n:] + str[:n]
 
def prefixMatch(dictionary, prefix):
    '''
        Returns list of words matched with prefix
    '''

    word_match = []
    for word in dictionary:
        if word.startswith(prefix):
            word_match.append(word)
    return word_match
 
def getPrefixForm(query):
    """
        Returns prefix form of the term (query)
    """

    chopped_query = query.split("*")
 
    if len(chopped_query) == 1:
        prefix = chopped_query[0]
    elif chopped_query[1] == '':
        prefix = chopped_query[0]
    elif chopped_query[0] == '':
        prefix = chopped_query[1]+'$'
    else:
        prefix = chopped_query[1]+'$'+chopped_query[0]
    
    return prefix
    
 
def createPermutermDictionary(dictionary):
    """
        Creates a perumterm indexing for the given dictionary
    """

    premutermDictionary = []
    for word in dictionary:
        word += '$'
        for i in range(len(word)):
            premutermDictionary.append(rotate(word,i))
    return premutermDictionary
 
def getActualWords(possible_rotated_words, query):
    """
        Returns the list of possible words from the permuterm index 
    """

    possible_words = []
 
    for rotated_words in possible_rotated_words:
        for i in range(len(rotated_words)):
            if rotate(rotated_words,i).endswith('$'):
                chopped_query = query.split("*")
                if len(chopped_query) == 1:
                    if chopped_query == rotate(rotated_words,i)[:-1]:
                        possible_words.append(rotate(rotated_words,i)[:-1])
                else:
                    if rotate(rotated_words,i)[:-1].startswith(chopped_query[0]) and rotate(rotated_words,i)[:-1].endswith(chopped_query[1]):
                        possible_words.append(rotate(rotated_words,i)[:-1])
                
                break
    return possible_words

def processWildCardSearch(query, keys):
    """
        Returns the possible list of words
    """

    permutermDictionary = createPermutermDictionary(keys)
    prefix = getPrefixForm(query)
    possible_rotated_words = prefixMatch(permutermDictionary, prefix)
    possibe_words = getActualWords(possible_rotated_words, query)

    return possibe_words


def buildQuery(possible_words):
    """
        Builds a query with the possible words. Eg - tok1 OR tok2 OR tok3
    """
    
    query = ["("]
    for token in possible_words:
        query.append(token)
        query.append("OR")

    query = query[:-1]
    query.append(")")

    return " ".join(query)
