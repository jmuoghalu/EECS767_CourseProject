import math, os, re, sys
from collections import OrderedDict

class IndexEntry:
    def __init__(self):
        self.term = ""
        self.doc_id = -1
        self.posting_list = PostingList()
        self.posting_size = 0

class PostingList:
    def __init__(self):
        self.doc_id = -1
        self.df = 0
        self.token_stream = None
        self.next = None
        self.size = 0

    def getTokenStream(self):
        None

    def countDocFrequency(self):
        None



if __name__ == '__main__':
    try:
        proc_doc_location = "../processed_testdoc/"
        proc_doc_location = "../testdoc/" # NOTE: files in this directory contain punctuation
        document_list = {}
        count = 1
        inverted_index = {}

        # build the unsorted inverted index
        # if a term appears in multiple documents, the DocIDs will be saved as a list
        # inverted_index = { term : [[DocID], TF] }
        for root, dirs, files in os.walk(proc_doc_location):
            for f in files:
                if f.endswith(".txt"):
                    document_list[f] = count

                    curr_file = open((proc_doc_location + f), "r", encoding="UTF8")
                    read_from_file = (re.sub(r"[^a-zA-Z0-9_ ]+", "", curr_file.read().lower())).split()
                    while(read_from_file):
                        for r in read_from_file:
                            try:
                                inverted_index[r][1] += 1
                            except KeyError:
                                inverted_index[r] = [[], 1]
                            inverted_index[r][0].append(count)
                        read_from_file = (re.sub(r"[^a-zA-Z0-9_ ]+", "", curr_file.read().lower())).split()

                    count += 1

        inverted_index = OrderedDict(sorted(inverted_index.items(), key=lambda t: t[0])) # sort the inverted index

        for x, [ys, z] in inverted_index.items():
            print( "{%s, %s, %s}" % (x, len(ys), z))


    except Exception as e:
        raise

        """
        To implement the stemmer and stopper, Python provides easily available stemmers and stoppers libraries that can be imported, created by the Natural Language Toolkit (NLTK). Each processed file is output to a new corresponding processed file. Once the file has been processed, each word is added to the dictionary array as a tuple containing the word and its document frequency, with a pointer to the posting list object that contains the document number, frequency, and a pointer to the next object, creating a linked list. After document preprocessing is done, the dictionary data is used to calculate the TF-IDF based ranking for each document. We are currently working on comparing the query and document vectors efficiently, and determining which data structures would be most beneficial to hold the vectors and inverted index.
        """
