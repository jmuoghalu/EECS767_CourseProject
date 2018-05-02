import math, os, re
from indexer import InvertedIndex as InvertedIndexClass

"""
    Dictionary: {term: idf}
    Dictionary: {term: [weights]}
"""

class VectorSpaceModel:
    def __init__(self, iic: InvertedIndexClass, index_basename):
        self.iic = iic
        self.terms_idf = {} # {term: IDF}
        self.terms_weights = {} # {term: [weights]}
        self.document_vectors = {} # [[docID: [weights]] # THIS VARIABLE DOES NOT NEED TO BE FILLED
        self.document_lengths = [] # [[docID, docLength]]
        self.index_basename = index_basename

        # using list instead of dictionary to preserver order
        for i in range(0, len(iic.document_list)):
            self.document_vectors[i] = [0 for i in range(0,len(iic.inverted_index))]
            self.document_lengths.append([(i+1), 0]) # [docID: docLength]

    def createEntireModel(self, iic: InvertedIndexClass):
        # for all of the inverted index terms and their posting lists, calculate the IDF values and the weights
        # Note: the inverted_index is sorted alphabetically after its creation
        doc_vec_index = 0
        for term,entry in iic.inverted_index.items():
            # calculate and save the IDF value for this term
            self.terms_idf[term] = entry.term_idf

            # initialize all weights as zero
            self.terms_weights[term] = [0 for i in range(0, len(iic.document_list))]

            # if the term exists in this document, update the weight to the actual value
            for docID, TF in entry.posting_list.items():
                # ex.) document #1 is located at index 0 in the terms_weights value list
                weight = self.terms_idf[term] * TF
                self.terms_weights[term][(docID-1)] = weight
                self.document_vectors[(docID-1)][doc_vec_index] = weight
                self.document_lengths[(docID-1)][1] += weight*weight

            doc_vec_index += 1

        self.computeDocWeights()


    def createModelRow(self, which_term):
        # fill the row of tf-idf weights for this parameter term
        """
            import re
            with open('abc') as f:
                for line in f:
                    if line.startswith('Key'):
                        keys = re.search(r'Key\s+(.*)',line).group(1).split("\t")
                    elif line.startswith(('Word','Letter')):
                        vals = re.search(r'(Word|Letter)\s+(.*)',line).group(2).split("\t")

            LineHere  w    x    y    z
            Key       a 1  b 2  c 3  d 4
            OrHere    00   01   10   11
            Word      as   box  cow  dig
        """

    def computeDocWeights(self):
        #complete the calculations of the document lengths by taking the square root
        for i in range(0, len(self.document_lengths)):
            self.document_lengths[i][1] = float("{0:.3f}".format(math.sqrt(self.document_lengths[i][1])))
