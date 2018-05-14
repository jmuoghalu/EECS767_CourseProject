import sys
sys.path.append("./nltk-3.3/")
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from re import sub as re_sub
from docproc import DocProcessor as DPClass
from indexer import InvertedIndex as InvertedIndexClass
from vsm import VectorSpaceModel as VSMClass
from query import Query as QueryClass
import os

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

def getDocuments(similarities, iic:InvertedIndexClass, proc_doc_location, query_terms):
    if not proc_doc_location[len(proc_doc_location)-1] == '/':
        proc_doc_location += "/"

    if not os.path.exists(proc_doc_location):
        print("The Input Directory Does Not Exist")
        return

    try:
        unprocessed_location = "../file_cache/unprocessed/" + os.path.basename(os.path.dirname(proc_doc_location))
        most_similar_documents = []
        # get the documents
            # similarities = [[docID, query-doc similarity]]
            # iic.document_list = [[docName, docID]]

        doc_list_already_checked = [False for i in range(len(iic.document_list))]
        for cs in similarities:
            for i in range(len(iic.document_list)):
                doc = iic.document_list[i]
                if not doc_list_already_checked[i]:
                    if cs[0] == doc[1]:
                        most_similar_documents.append(doc[0])
                        doc_list_already_checked[i] = True

        document_titles = ["" for i in range(0, len(most_similar_documents))]
        document_snapshots = ["" for i in range(0, len(most_similar_documents))] # the first appearance of the query
        for root, dirs, files in os.walk(unprocessed_location):
            for i in range(0, len(most_similar_documents)):
                name = most_similar_documents[i]
                for f in files:
                    # search directory for file name without extension
                    # take the file, and replace the index with it
                    if name == os.path.splitext(f)[0]:
                        document_titles[i] = dp.retrieveDocTitle(unprocessed_location + "/" + f)
                        document_snapshots[i] = dp.retrieveDocSnapshot(unprocessed_location + "/" + f, query_terms)
                        most_similar_documents[i] = f
            break

        return [unprocessed_location, most_similar_documents, document_titles, document_snapshots]

    except Exception as e:
        raise()



if __name__ == "__main__":
    try:
        doc_basename = "docsnew" # the actual name of the folder containing the processed files
        doc_location = "../file_cache/processed/" + doc_basename

        dp = DPClass()
        #dp.runDocProc("../../file_cache/unprocessed/" + doc_basename)
        iic = InvertedIndexClass()
        #iic.createInvertedIndex("../file_cache/processed/" + doc_basename)
        iic.loadInvertedIndex("../file_cache/processed/" + doc_basename)
        stemmer = PorterStemmer()

        continueLoop = True

        print("Welcome to the Search Engine\n")
        while continueLoop:
            fromUser = ""
            user_query = ""
            print("\n\nSelect from the Following Options:\n\t1.) Search\n\t2.) Exit")
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

                vsm = VSMClass(iic, doc_basename)
                qr = QueryClass(query, vsm)
                qr.computeSimilarities(10)

                # first index = location of unprocessed documents; second index = list of documents in order of similarity > 0
                location_and_documents = getDocuments(qr.all_similarities, iic, doc_location, query)

                if len(location_and_documents[1]) > 0:
                    print("\nResults:")
                    for i in range(0, len(location_and_documents[1])):
                        # NOTE: this might be yielding an encoding error
                        try:
                            print("\t\tURL:\t{0}".format(location_and_documents[1][i]))
                            print("\t\tTitle:\t{0}".format(location_and_documents[2][i]))
                            print("\t\tSnapshot:\t{0}".format(location_and_documents[3][i]))
                            print("")
                        except Exception as e:
                            print("Encoding Error")
                else:
                    print("\nThere are no relevant results.")

            elif from_user == "2":
                print("Goodbye.")
                break

            else:
                print("\nInvalid Input.")

    except Exception as e:
        raise()
