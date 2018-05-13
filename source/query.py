import math, os
from indexer import InvertedIndex as InvertedIndexClass
from vsm import VectorSpaceModel as VSMClass

class Query:
    def __init__(self, query_terms, vsm: VSMClass):
        self.query_vector = {} # {term: idf} # idf is 0 if the query term is not in the index
        self.flag_term_in_vsm = {query_terms[i]: False for i in range(len(query_terms))}
        self.document_lengths = vsm.document_lengths
        self.query_length = 0
        self.vsm = vsm

        # [[docID, query-doc similarity]]
        self.all_similarities = [[(i+1), 0] for i in range(0,len(self.vsm.document_lengths))]

        # query_terms = [terms]
        # to shorten the query vector, only add the weights for terms that appear in the query
        for i in range(len(query_terms)):
            qt = query_terms[i]
            qt_in_index = False
            # make sure the word actually exists within the vector model and inverted index
            if not (qt in self.vsm.terms_weights):
                qt_in_index = self.vsm.createModelRow(qt)
            else:
                qt_in_index = True # this term is in the index, and the weights have already been calculated

            if qt_in_index:
                self.flag_term_in_vsm[qt] = True
                qt_idf = self.vsm.terms_idf[qt]
                self.query_vector[qt] = qt_idf
                self.query_length += qt_idf*qt_idf
            else: # this search term is not in the index, so mark a zero in the query vector
                self.query_vector[qt] = 0

        # in the relevance feedback version of the code, fill the entire query vector
        for term in self.vsm.terms_weights.keys():
            if term not in self.query_vector.keys():
                self.query_vector[term] = 0

        # finish computing the query length
        self.query_length = float("{0:.3f}".format(math.sqrt(self.query_length)))

    def computeSimilarities(self):
        self.all_similarities = [[(i+1), 0] for i in range(0,len(self.vsm.document_lengths))]

        # populate the list of similarities, which is ordered by the dataset's docID's
        for qv, qv_idf in self.query_vector.items():
            # retreive the list of all tf-idf weights for the current query
            if self.flag_term_in_vsm[qv]:
                term_row = self.vsm.terms_weights[qv]
                for i in range(0, len(term_row)): # i = (docID-1)
                    self.all_similarities[i][1] += qv_idf * term_row[i]


        # complete the similarity calculation by dividing the value by the product of the two vectors' lengths
        for i in range(0, len(self.all_similarities)):
            if not ((self.document_lengths[i][1] == 0) or self.query_length == 0):
                self.all_similarities[i][1] = \
                    float("{0:.3f}".format(self.all_similarities[i][1] / (self.document_lengths[i][1] * self.query_length)))

        # lastly, sort the similarities
        self.all_similarities = sorted(self.all_similarities, key=lambda l:l[1], reverse=True)

        # drop the similarities if they == 0
        i = 0
        updated_similarities = []
        while not (i == (len(self.all_similarities))):
            if self.all_similarities[i][1] == 0:
                break
            updated_similarities.append([self.all_similarities[i][0], self.all_similarities[i][1]])
            i += 1
        self.all_similarities = updated_similarities[0:10]



    def relevanceFeedback(self, rel_and_irrel):

        # rel_and_irrel is a list of booleans corresponding to self.all_similarities
        # the indices marked True are the relevant documents, and False means irrelevant

        self.query_length = 0
        alpha = 1
        beta = 0.5
        gamma = 0

        # separate the relevant and irrelevant documents
        all_rel = []
        all_irrel = []
        for i in range(len(rel_and_irrel)):
            if rel_and_irrel[i]:
                all_rel.append(i)
            else:
                all_irrel.append(i)

        # update the query vector using the full document vectors
        # NOTE: this relevance feedback function is using the full vector model
        for qt in self.vsm.terms_weights.keys():

            try:
                self.query_vector[qt] = alpha * self.query_vector[qt]
            except KeyError as e:
                self.query_vector[qt] = 0

            # update the relevant document weights
            for i in range(len(all_rel)):
                # which_similar_doc = [docId, similarity_value]
                which_similar_doc = self.all_similarities[all_rel[i]]
                self.query_vector[qt] += (beta / (len(all_rel))) * self.vsm.terms_weights[qt][which_similar_doc[0]-1]

            # update the irrelevant document weights
            for i in range(len(all_irrel)):
                which_similar_doc = self.all_similarities[all_irrel[i]]
                self.query_vector[qt] -= (gamma / (len(all_irrel))) * self.vsm.terms_weights[qt][which_similar_doc[0]-1]

            self.query_vector[qt] = float("{0:.3f}".format(self.query_vector[qt]))

            self.query_length += self.query_vector[qt] * self.query_vector[qt]

        # finish computing the query length
        self.query_length = float("{0:.3f}".format(math.sqrt(self.query_length)))
