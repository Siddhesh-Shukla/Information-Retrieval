from nltk.tokenize import word_tokenize
from utils.preprocess import getCleanQueryToken

class BooleanModel:
    """
        Traditional Boolean Query Model, handles - AND OR NOT operations
    """

    def __init__(
        self, 
        corpus_size: int,
        inverted_index: dict,
        norm_type:str
    ) -> None:

        """
            Initializing necessary parameters and indexes
            corpus_size: Number of documents 
            operators: AND OR NOT (
        """


        self.corpus_size = corpus_size
        self.inverted_index = inverted_index
        self.operators = ["AND", "OR", "NOT", "("]
        self.normalization_type=norm_type

    def __str__(self) -> str:
        return "Boolean Query Model"
    
    def _AND(self, lOp, rOp):
        """
            Performs 'lOp AND rOp' operation
        """

        result = {
            "title": list(set(lOp["title"]) & set(rOp["title"])),
            "meta": list(set(lOp["meta"]) & set(rOp["meta"])),
            "characters": list(set(lOp["characters"]) & set(rOp["characters"])),
            "body": list(set(lOp["body"]) & set(rOp["body"]))
        }

        return result
    
    def _OR(self, lOp, rOp):
        """
            Performs 'lOp OR rOp' operation
        """
        
        result = {
            "title": list(set(lOp["title"]) | set(rOp["title"])),
            "meta": list(set(lOp["meta"]) | set(rOp["meta"])),
            "characters": list(set(lOp["characters"]) | set(rOp["characters"])),
            "body": list(set(lOp["body"]) | set(rOp["body"]))
        }

        return result
        
    
    def _NOT(self, Op):
        """
            Performs 'NOT Op' operation
        """

        docIDs = set(range(self.corpus_size))
        
        result = {
            "title": list(docIDs -  set(Op["title"])),
            "meta": list(docIDs -  set(Op["meta"])),
            "characters": list(docIDs -  set(Op["characters"])),
            "body": list(docIDs -  set(Op["body"]))
        }

        return result


    def parse_query(self, query):
        """
            Parsers the query and returns a pre-processed query

            Parameters -
            query: query in tokenized format

            Return-
            result of the operations 

        """

        operand_stack = []
        operator_stack = []

        for term in query:
            if (term not in self.operators) and (term != ')'):
                clean_token = getCleanQueryToken(term, normalization_type=self.normalization_type)

                if clean_token in self.inverted_index.keys():
                    operand_stack.append(self.inverted_index[clean_token])
                else:
                    operand_stack.append({"title": [], "meta": [], "characters": [], "body": []})
            
            elif term in self.operators:
                operator_stack.append(term)
            
            else:
                while(operator_stack[-1] != "("):
                    if (operator_stack[-1] == "NOT"):
                        Op = operand_stack.pop()
                        operator_stack.pop()
                        result = self._NOT(Op)
                        operand_stack.append(result)
                    
                    elif (operator_stack[-1] == "OR"):
                        rOp = operand_stack.pop()
                        lOp = operand_stack.pop()
                        operator_stack.pop()

                        result = self._OR(lOp, rOp)
                        operand_stack.append(result)
                    
                    else:
                        rOp = operand_stack.pop()
                        lOp = operand_stack.pop()
                        operator_stack.pop()

                        result = self._AND(lOp, rOp)
                        operand_stack.append(result)

                operator_stack.pop() # pop "("
            
        return operand_stack[-1]


    def process_query(self, query):
        """
            Processes the query and returns the result
            Parameters -
            query: query in string

            Return-
            result of the operations
        """

        tokenized_query = word_tokenize(query)
        return self.parse_query(tokenized_query)

