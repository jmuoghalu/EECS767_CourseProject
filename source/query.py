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



def debugPrint(query: Query, vsm: VSMClass, iic: InvertedIndexClass):

    print("\n\nInverted Index:")
    for term, index in iic.inverted_index.items():
        print(end="" "{ %s , %s , %s } " % (index.term, len(index.docID_list), index.term_tf) )
        first = True
        if len(index.term) < 4:
            print(end="" "\t")
        print(end="" "\t\t -> ")

        for docID, TF in index.posting_list.items():
            if not first:
                print(end="" " -> ")
            print(end="" "[%s | %s]" % (docID, TF))
            first = False
        print("")

    print("\n\nVector Space Model")
    print("term\t\tIDF\t\t", end='')
    for x in iic.document_list:
        print(x[0] + "\t\t", end='')
    print()

    for term, IDF in vsm.terms_idf.items():
        if len(term) < 8:
            print(term + "\t\t", end='')
        else:
            print(term + "\t", end='')
        print(str(IDF) + "\t\t", end='')

        for weight in vsm.terms_weights[term]:
            print(str(weight) + "\t\t", end='')

        print()

    #"""
    print("\n\nDocument Lengths")
    for i in range(0, len(vsm.document_vectors)):
        """doc = vsm.document_vectors[i]
        print(end='' "\t[ %s" % (str(doc[0])))
        for j in range(1,len(doc)):
            print(end='' ", %s" % (str(doc[j])))
        print("] == |%s|" % (vsm.document_lengths[i][1]))"""
        print("\t[...] == |%s|" % (vsm.document_lengths[i][1]))
    #"""

    #"""
    print("\n\nQuery")
    print("Terms: %s" % (query.query_vector.keys()))
    print(end='' "Result: [D%s, %s]" %
        (query.all_similarities[0][0], query.all_similarities[0][1]))
    for i in range(1, len(query.all_similarities)):
        print(end='' ", [D%s, %s]" %
            (query.all_similarities[i][0], query.all_similarities[i][1]))
    #"""
    print("\n\n")


if __name__ == "__main__":
    try:
        proc_doc_location = "../testdoc"
        iic = InvertedIndexClass()
        iic.createInvertedIndex(proc_doc_location)
        vsm = VSMClass(iic)

        query1 = ["silver", "truck"]
        qr1 = Query(query1, vsm)
        debugPrint(qr1, vsm, iic)

        query2 = ["damaged", "truck"]
        qr2 = Query(query2, vsm)
        debugPrint(qr2, vsm, iic)


    except Exception as e:
        raise()

        """
        To implement the stemmer and stopper, Python provides easily available stemmers and stoppers libraries that can be imported, created by the Natural Language Toolkit (NLTK). Each processed file is output to a new corresponding processed file. Once the file has been processed, each word is added to the dictionary array as a tuple containing the word and its document frequency, with a pointer to the posting list object that contains the document number, frequency, and a pointer to the next object, creating a linked list. After document preprocessing is done, the dictionary data is used to calculate the TF-IDF based ranking for each document. We are currently working on comparing the query and document vectors efficiently, and determining which data structures would be most beneficial to hold the vectors and inverted index.
        """
