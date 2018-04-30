import math, os
from indexer import InvertedIndex as InvertedIndexClass

"""
    Dictionary: {term: idf}
    Dictionary: {term: [weights]}
"""

class VectorSpaceModel:
    def __init__(self, iic: InvertedIndexClass):
        self.terms_idf = {} # {term: IDF}
        self.terms_weights = {} # {term: [weights]}
        self.document_vectors = {} # [[docID: [weights]] # THIS VARIABLE DOES NOT NEED TO BE FILLED
        self.document_lengths = [] # [[docID, docLength]]


        # using list instead of dictionary to preserver order
        for i in range(0, len(iic.document_list)):
            self.document_vectors[i] = [0 for i in range(0,len(iic.inverted_index))]
            self.document_lengths.append([(i+1), 0]) # [docID: docLength]

        # for all of the inverted index terms and their posting lists, calculate the IDF values and the weights
        # Note: the inverted_index is sorted alphabetically after its creation
        doc_vec_index = 0
        for term,entry in iic.inverted_index.items():
            # calculate and save the IDF value for this term
            self.terms_idf[term] = float("{0:.3f}".format(math.log10( len(iic.document_list) / len(entry.docID_list) )))

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

        #complete the calculations of the document lengths by taking the square root
        for i in range(0, len(self.document_lengths)):
            self.document_lengths[i][1] = float("{0:.3f}".format(math.sqrt(self.document_lengths[i][1])))