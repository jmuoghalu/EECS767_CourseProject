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
import urllib.request
import json, os, string

def getDocumentsWebDriver(similarities, iic:InvertedIndexClass, dp:DPClass, proc_doc_location, query_terms):

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



def WebDriverRelevanceFeedback(qr:QueryClass, iic:InvertedIndexClass, proc_doc_location, query_terms):
    # if returning n results, initialize an n-sized list of booleans as true
    rel_and_irrel = [False for i in range(len(location_and_documents[1]))]
    # place the HTML checkboxes in a list
        # checkboxes marked true means that the boolean at that index should be marked true

    qr.relevanceFeedback(rel_and_irrel)
    qr.computeSimilarities(10)
    return getDocumentsWebDriver(qr, iic, proc_doc_location, query_terms)


if __name__ == "__main__":

    output = {}
    try:
        try:
            doc_basename = "newly_crawled" # the actual name of the folder containing the processed files
            doc_location = "../file_cache/processed/" + doc_basename

            dp = DPClass()
            iic = InvertedIndexClass()
            iic.loadInvertedIndex(doc_location)

            vsm = VSMClass(iic, doc_basename)
            vsm.createEntireModel()
            stemmer = PorterStemmer()

            english_file = open("./nltk-3.3/nltk_data/corpora/stopwords/english", "r", encoding="UTF8")
            english_words = english_file.read().strip().split()
            english_file.close()

            if len(sys.argv) < 3:
                print("You Need to Give the Search Term and the Feedback String")
                sys.exit()

            arguments = ""
            query = []
            # argument 0 is the file name
            for argi in sys.argv[1:(len(sys.argv)-1)]:
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

            print(query)
            rel_and_irrel = [False for i in range(len(location_and_documents[1]))]
            feedback_string = sys.argv[len(sys.argv)-1]
            relevant = feedback_string.split("_")
            for i in range(len(relevant)):
                rel_and_irrel[int(relevant[i])-1] = True

            qr.relevanceFeedback(rel_and_irrel)
            qr.computeSimilarities(10)

            location_and_documents = getDocumentsWebDriver(qr.all_similarities, iic, dp, doc_location, query)

            output = {}
            if len(location_and_documents[1]) > 0:
                letter_keys = list(string.ascii_lowercase[:len(location_and_documents[1])])
                for i in range(0, len(location_and_documents[1])):
                    # NOTE: this might be yielding an encoding error
                    output[letter_keys[i]] = {}
                    try:
                        output[letter_keys[i]]["url"] = location_and_documents[1][i]
                        if doc_basename == "docsnew":
                            output[letter_keys[i]]["url"] = "http://en.wikipedia.org/wiki/" + output[letter_keys[i]]["url"]
                        output[letter_keys[i]]["name"] = location_and_documents[2][i]
                        output[letter_keys[i]]["snapshot"] = location_and_documents[3][i]
                    except Exception as e:
                        output[letter_keys[i]]["url"] = "ERROR"
                        output[letter_keys[i]]["name"] = "ERROR"
                        output[letter_keys[i]]["snapshot"] = "ERROR"

        except Exception as e:
            output = {"ERROR MESSAGE": "Python Exception:\t{0}".format(str(e))}

        # print the documents so that the web page can see and access them
        print(json.dumps(output, sort_keys=True, ))

    except KeyboardInterrupt:
        sys.exit()
