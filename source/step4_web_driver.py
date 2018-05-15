import sys
sys.path.append("/nltk-3.3/")
sys.path.append("/home/j286m692/EECS_767/EECS767_CourseProject/source/nltk-3.3/")
sys.path.append("/home/j286m692/nltk_data/")
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from re import sub as re_sub
from docproc import DocProcessor as DPClass
from indexer import InvertedIndex as InvertedIndexClass
from vsm import VectorSpaceModel as VSMClass
from query import Query as QueryClass
import json, os


def getDocumentsWebDriver(similarities, iic:InvertedIndexClass, dp:DPClass, proc_doc_location, query_terms):

    if not proc_doc_location[len(proc_doc_location)-1] == '/':
        proc_doc_location += "/"

    if not os.path.exists(proc_doc_location):
        return ("The Input Directory Does Not Exist")

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
    output = {}
    try:
        doc_basename = "newly_crawled" # the actual name of the folder containing the processed files
        doc_location = "../file_cache/processed/" + doc_basename

        dp = DPClass()
        iic = InvertedIndexClass()
        iic.loadInvertedIndex("../file_cache/processed/" + doc_basename)
        vsm = VSMClass(iic, doc_basename)

        stemmer = PorterStemmer()

        english_file = open("./nltk-3.3/nltk_data/corpora/stopwords/english", "r", encoding="UTF8")
        english_words = english_file.read().strip().split()
        english_file.close()

        if len(sys.argv) < 2:
            output = {"ERROR MESSAGE": "You Need to Give a Search Term"}

        else:
            arguments = ""
            query = []
            # argument 0 is the file name
            for argi in sys.argv[1:]:
                arguments += "   {0}  ".format(argi)

            formatted_arguments = (re_sub(r"[^a-zA-Z0-9_ ]+", "", arguments.lower().strip())).split()
            for i in range(0, len(formatted_arguments)):
                if formatted_arguments[i] not in english_words:
                    query.append(stemmer.stem(formatted_arguments[i]))

            qr = QueryClass(query, vsm)
            qr.computeSimilarities(10)

            # first index = location of unprocessed documents; second index = list of document titles ; third index = list of documents in order of similarity > 0
            # if the list at index 1 is empty, then there are no similar documents
            location_and_documents = getDocumentsWebDriver(qr.all_similarities, iic, dp, doc_location, query)
            if len(location_and_documents[1]) > 0:
                for i in range(0, len(location_and_documents[1])):
                    # NOTE: this might be yielding an encoding error
                    output[str(i+1)] = {}
                    try:
                        output[str(i+1)]["url"] = location_and_documents[1][i]
                        if doc_basename == "docsnew":
                            output[str(i+1)]["url"] = "http://en.wikipedia.org/wiki/" + output[str(i+1)]["url"]
                        output[str(i+1)]["name"] = location_and_documents[2][i]
                        output[str(i+1)]["snapshot"] = location_and_documents[3][i]
                    except Exception as e:
                        output[str(i+1)]["url"] = "ERROR"
                        output[str(i+1)]["name"] = "ERROR"
                        output[str(i+1)]["snapshot"] = "ERROR"



    except Exception as e:
        output = {"ERROR MESSAGE": "Python Exception:\t{0}".format(str(e))}

    print(json.dumps(output, sort_keys=True))
