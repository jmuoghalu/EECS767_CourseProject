import math, os
from indexer import InvertedIndex as InvertedIndexClass
from vsm import VectorSpaceModel as VSMClass

class Query:
    def __init__(self, query_terms, vsm: VSMClass):
        self.query_vector = {} # {term: idf} # idf is 0 if the query term is not in the index
        self.query_length = 0

        # helper variable for determining if this query term has data within the vector model
        self.flag_term_in_vsm = {query_terms[i]: False for i in range(len(query_terms))}

        self.proximity_scores = {} # {term: proximity_score} # used in term proximity

        # allowing for easier access of document information
        self.vsm = vsm
        self.document_lengths = vsm.document_lengths

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

            if qt_in_index: # the query term exists in the model, so update the query vector
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



    def computeSimilarities(self, totalToTake):
        self.all_similarities = [[(i+1), 0] for i in range(0,len(self.vsm.document_lengths))]

        # populate the list of similarities, which is ordered by the dataset's docID's
        for qv, qv_idf in self.query_vector.items():
            # retreive the list of all tf-idf weights for the current query
            try:
                if self.flag_term_in_vsm[qv]:
                    term_row = self.vsm.terms_weights[qv]
                    for i in range(0, len(term_row)): # i = (docID-1)
                        self.all_similarities[i][1] += qv_idf * term_row[i]
            except KeyError:
                pass


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
            if not self.all_similarities[i][1] == 0:
                updated_similarities.append([self.all_similarities[i][0], self.all_similarities[i][1]])
            i += 1

        # the program will only take a specific number of the most similar documents
        if totalToTake > len(updated_similarities):
            self.all_similarities = updated_similarities
        else:
            self.all_similarities = updated_similarities[0:totalToTake]



    # by the time this function is called, the similarities vector will have already been populated
    def termProximity(self, proc_doc_location):

        if not proc_doc_location[len(proc_doc_location)-1] == '/':
            proc_doc_location += "/"

        if not os.path.exists(proc_doc_location):
            return ("The Input Directory Does Not Exist")

        # intiialize important variables
        query_terms = []
        self.proximity_scores = {}
        for qt in self.query_vector.keys():
            query_terms.append(qt)
            self.proximity_scores[qt] = 0

        # iterate through the vector of most-similar documents
        document_scores = []
        for i in range(len(self.all_similarities)):
            document_scores.append(1) # save the score for this document
            current_docID = self.all_similarities[i][0]
            current_doc_name = self.vsm.documents[current_docID-1][0]

            # retrieve this document
            file = open((proc_doc_location + current_doc_name + ".txt"), "r", encoding="UTF8")

            # every word in this file will be a list index
            file_text = file.read().strip().split()

            # a dictionary of every occurrence of a query term in the file
            # each vlaue corresponds to where in the file query term occurs
            # use a dictionary so that key accesses will only be valid for terms that appear in the query
            qt_single_occurrences = {query_terms[i]: [] for i in range(len(query_terms))}
            for j in range(len(file_text)):
                if file_text[j] in query_terms:
                    try:
                        qt_single_occurrences[file_text[j]].append(j)
                    except KeyError as e:
                        pass

            # make sure that every query term occurs in this document
            # if not, then remove the term from the query_terms list, and consider term proximity for the other terms
            j = 0
            while j < len(query_terms):
                if len(qt_single_occurrences[query_terms[j]]) == 0:
                    try:
                        del qt_single_occurrences[query_terms[j]]
                        query_terms.pop(j)
                        continue
                    except Exception as e:
                        pass
                j += 1


            # if none of the query terms were found in this document, then continue
            if qt_single_occurrences == {}:
                continue

            # every occurrence of every query term has been recorded for this document
            # merge the sublists and sort them, all while keeping track of which position corresponds to which word in the query
            # afterwards, sort by the locations, not the words
            qt_merged = []
            for qt in qt_single_occurrences.keys():
                for j in range(len(qt_single_occurrences[qt])):
                    qt_merged.append((qt, qt_single_occurrences[qt][j]))
            qt_merged = sorted(qt_merged, key=lambda qt: qt[1])

            # the term occurrences are now ordered, so if two adjacent tuples correspond to a single query term appearing close together without any of the others in between, then drop one of the entries
                # if the term is the first one in the query, then drop the lowest numbered occurrence of the two
                # if the term is the last one in the query, then drop the highest numbered occurrence of the two
                # else, search for three adjacent tuples, and drop the middle one
            # this is because we want to analyze the term proximities as the terms relate to each other, not to themselves
            j = 0
            while j < (len(qt_merged) - 1):
                position_j = qt_merged[j]
                if position_j[0] == query_terms[0]:
                    next_position = qt_merged[j+1]
                    if position_j[0] == next_position[0]:
                        qt_merged.pop(j)
                        continue
                    j += 1
                elif position_j[0] == query_terms[len(query_terms)-1]:
                    next_position = qt_merged[j+1]
                    if position_j[0] == next_position[0]:
                        qt_merged.pop(j+1)
                        continue
                    j += 1
                else:
                    # if there are three adjacent tuples that correspond to a single query term
                    if (j + 2) < len(qt_merged):
                        next_position = qt_merged[j+1]
                        after_next = qt_merged[j+2]
                        if position_j[0] == next_position[0] == after_next[0]:
                            qt_merged.pop(j+1)
                            continue
                j += 1

            # we now have a relatively small list that can be used to score term proximities
            # for every tuple in the list, calculate the minimum distance between the current term and the next term in the query
            minimum_distances = {query_terms[k]:0 for k in range(len(query_terms))}
            for k in range(len(qt_merged)-1):
                current_term = qt_merged[k]
                for m in range(k+1, len(qt_merged)):
                    other_term = qt_merged[m]

                    # move on if these are the same terms
                    if not (current_term[0] == other_term[0]):
                        this_distance = abs(current_term[1]-other_term[1])

                        if (minimum_distances[current_term[0]] == 0) or (minimum_distances[current_term[0]] > this_distance):
                            minimum_distances[current_term[0]] = this_distance

            # at this point, we have a dictionary that tells us the minimum distance within the document of a word in the query and the next unique word in the query
            # we will score this document by inversing each distance and taking the sum of these values
                # we use inverse because the smaller the distance, then the closer the two words
            for dv in minimum_distances.values():
                if not dv == 0:
                    document_scores[i] += (1/dv)

            """
            print("{0}{1}.txt".format(proc_doc_location, current_doc_name.encode(encoding='utf_8', errors='ignore')))
            print(minimum_distances)
            print("Score = {0}".format(document_scores[i]))
            """
        return document_scores



    # update the document similarities according to the previously calculated proximity scores
    def computeProximitySimilarities(self, document_scores, totalToTake):
        for i in range(len(self.all_similarities)):
            self.all_similarities[i][1] *= document_scores[i]

        # lastly, sort the similarities
        self.all_similarities = sorted(self.all_similarities, key=lambda l:l[1], reverse=True)

        # drop the similarities if they == 0
        i = 0
        updated_similarities = []
        while not (i == (len(self.all_similarities))):
            if not self.all_similarities[i][1] == 0:
                updated_similarities.append([self.all_similarities[i][0], self.all_similarities[i][1]])
            i += 1

        if totalToTake > len(updated_similarities):
            self.all_similarities = updated_similarities
        else:
            self.all_similarities = updated_similarities[0:totalToTake]


    # by the time this function is called, the similarities vector will have already been populated
    def relevanceFeedback(self, rel_and_irrel):

        # rel_and_irrel is a list of booleans corresponding to self.all_similarities
        # the indices marked True are the relevant documents, and False means irrelevant

        # relevance feedback data will be computed using Rocchio Algorithm
        self.query_length = 0
        alpha = 1
        beta = 0.75
        gamma = 0.25

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

            # update query vector 
            self.query_vector[qt] = float("{0:.3f}".format(self.query_vector[qt]))
            self.query_length += self.query_vector[qt] * self.query_vector[qt]

        # finish computing the query length
        self.query_length = float("{0:.3f}".format(math.sqrt(self.query_length)))
