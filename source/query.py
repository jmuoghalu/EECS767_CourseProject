import math, os
from indexer import InvertedIndex as InvertedIndexClass
from vsm import VectorSpaceModel as VSMClass

class Query:
    def __init__(self, query_terms, vsm: VSMClass):
        self.query_vector = {} # {term: idf}
        self.query_length = 0

        # [[docID, query-doc similarity]]
        self.all_similarities = [[(i+1), 0] for i in range(0,len(vsm.document_lengths))]

        # query_terms = [terms]
        # to shorten the query vector, only add the weights for terms that appear in the query
        for qt in query_terms:
            # make sure the word actually exists within the vector model and inverted index
            if qt in vsm.terms_weights:
                qt_idf = vsm.terms_idf[qt]
                self.query_vector[qt] = qt_idf
                self.query_length += qt_idf*qt_idf

        # finish computing the query length
        self.query_length = float("{0:.3f}".format(math.sqrt(self.query_length)))

        # populate the list of similarities, which is ordered by the dataset's docID's
        for qv, qv_idf in self.query_vector.items():
            # retreive the list of all tf-idf weights for the current query
            term_row = vsm.terms_weights[qv]
            for i in range(0, len(term_row)): # i = (docID-1)
                self.all_similarities[i][1] += qv_idf * term_row[i]

        # complete the similarity calculation by dividing the value by the product of the two vectors' lengths
        for i in range(0, len(self.all_similarities)):
            self.all_similarities[i][1] = \
                float("{0:.3f}".format(self.all_similarities[i][1] / (vsm.document_lengths[i][1] * self.query_length)))

        # lastly, sort the similarities
        self.all_similarities = sorted(self.all_similarities, key=lambda l:l[1], reverse=True)
