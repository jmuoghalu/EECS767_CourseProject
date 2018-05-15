import math, os, re
from indexer import InvertedIndex as InvertedIndexClass

class VectorSpaceModel:
    def __init__(self, iic: InvertedIndexClass, index_basename):
        self.iic = iic
        self.terms_idf = {} # {term: IDF}
        self.terms_weights = {} # {term: [weights]}

        # THIS VARIABLE IS ONLY FILLED WHEN THE createEntireModel FUNCTION IS cALLED
        self.document_vectors = {} # {docID: [weights]}

        # allows for more easy access of document information
        self.documents = iic.document_list
        self.document_lengths = iic.document_lengths
        self.index_basename = index_basename
        

    # for all of the inverted index terms and their posting lists, calculate the IDF values and the weights
    # Note: the inverted_index is sorted alphabetically after its creation
    def createEntireModel(self):
        for doc in self.iic.document_list:
            self.document_vectors[doc[1]-1] = [0 for i in range(len(self.iic.inverted_index.values()))]

        doc_vec_index = 0 # helper variable for traversing and filling the document vectors
        for term,entry in self.iic.inverted_index.items():
            # calculate and save the IDF value for this term
            self.terms_idf[term] = entry.term_idf

            # initialize all weights as zero
            self.terms_weights[term] = [0 for i in range(0, len(self.iic.document_list))]

            # if the term exists in this document, update the weight to the actual value
            for docID, TF in entry.posting_list.items():
                # ex.) document #1 is located at index 0 in the terms_weights value list
                weight = entry.term_idf * TF
                self.terms_weights[term][(docID-1)] = weight
                self.document_vectors[(docID-1)][doc_vec_index] = weight

            doc_vec_index += 1



    # fill the row of tf-idf weights for this parameter term only
    def createModelRow(self, which_term):
        entry = None
        try:
            entry = self.iic.inverted_index[which_term]
        except KeyError: # the parameter term does not exist in the inverted index
            return False

        # check if this row has already been created (i.e. the search engine has already built the entire model)
        try:
            self.terms_idf[which_term]
            self.terms_weights[which_term]
        except KeyError:
            # calculate and save the IDF value for this term
            self.terms_idf[which_term] = entry.term_idf

            # initialize all weights as zero
            self.terms_weights[which_term] = [0 for i in range(0, len(self.iic.document_list))]

            # if the term exists in this document, update the weight to the actual value
            for docID, TF in entry.posting_list.items():
                # ex.) document #1 is located at index 0 in the terms_weights value list
                self.terms_weights[which_term][(docID-1)] = entry.term_idf * TF

        return True
