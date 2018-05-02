from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from re import sub as re_sub
from docproc import DocProcessor as DPClass
from indexer import InvertedIndex as InvertedIndexClass
from vsm import VectorSpaceModel as VSMClass
from query import Query as QueryClass
import sys

def debugPrint(query: QueryClass, vsm: VSMClass, iic: InvertedIndexClass):

    """
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

    print("\n\nDocument Lengths")
    for i in range(0, len(vsm.document_vectors)):
        doc = vsm.document_vectors[i]
        print(end='' "\t[ %s" % (str(doc[0])))
        for j in range(1,len(doc)):
            print(end='' ", %s" % (str(doc[j])))
        print("] == |%s|" % (vsm.document_lengths[i][1])) #
        print("\t[...] == |%s|" % (vsm.document_lengths[i][1]))
    #"""

    #"""
    print("\n\nQuery")
    print("Terms: %s" % (query.query_vector.keys()))
    print(end='' "Result:\n\t[D%s,\t%s]" %
        (query.all_similarities[0][0], query.all_similarities[0][1]))
    for i in range(1, len(query.all_similarities)):
        print(end='' ",\n\t[D%s,\t%s]" %
            (query.all_similarities[i][0], query.all_similarities[i][1]))
    #"""
    print("\n\n")


if __name__ == "__main__":
    try:
        #doc_basename = "docsnew" # the actual name of the folder containing the processed files
        doc_basename = "testdoc" # the actual name of the folder containing the processed files
        doc_location = "../file_cache/processed/" + doc_basename

        #dp = DPClass()
        #dp.runDocProc(doc_location)
        iic = InvertedIndexClass()
        iic.createInvertedIndex(doc_location)
        iic.loadInvertedIndex(doc_location)
        vsm = VSMClass(iic)
        stemmer = PorterStemmer()

        continueLoop = True
        fromUser = ""

        print("Welcome to the Search Engine\n")
        while continueLoop:
            print("Select from the Following Options:\n\t1.) Search\n\t2.) Exit")
            from_user = input("Your Choice: ")

            if from_user == "1":
                # NOTE: this function is raw_input for Python 2.x
                print("\nSearching through the ''{0}'' File Cache:".format(doc_basename))
                user_query = input("What Is Your Query?:  ")
                formatted_query = (re_sub(r"[^a-zA-Z0-9_ ]+", "", user_query.lower().strip())).split()
                query = []
                for i in range(0, len(formatted_query)):
                    if formatted_query[i] not in stopwords.words("english"):
                        query.append(stemmer.stem(formatted_query[i]))

                qr = QueryClass(query, vsm)
                debugPrint(qr, vsm, iic)

            elif from_user == "2":
                print("Goodbye.")
                break

            else:
                print("\nInvalid Input.")


        """
            # TODO:
                1.) take the sorted similarity list, retrieve the document ID's, use the ID's to get the document basenames, and use the basenames to retrieve pages from the document source folder (NOT THE PROCESSED FOLDER)
        """

    except Exception as e:
        raise()
