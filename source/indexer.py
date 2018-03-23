import math, os, re, sys
from collections import OrderedDict

class IndexEntry:
    def __init__(self):
        self.term = ""
        self.docID_list = [] # the size of this list is the term's DF
        self.term_tf = 0
        self.posting_list = {}


if __name__ == '__main__':
    try:
        proc_doc_location = "../processed_testdoc/"
        proc_doc_location = "../testdoc/" # NOTE: files in this directory contain punctuation
        document_list = {}
        current_docID = 1
        inverted_index = {}

        """
        build the unsorted inverted index
        if a term appears in multiple documents, the DocIDs will be saved as a list
            inverted_index = { term : IndexEntry }
            IndexEntry.posting_list = { docID : TF }
        """
        for root, dirs, files in os.walk(proc_doc_location):
            for f in files:
                if f.endswith(".txt"):
                    document_list[f] = current_docID
                    curr_file = open((proc_doc_location + f), "r", encoding="UTF8")

                    # read a line; convert to lowercase; remove punctuation, and separate the words
                    read_from_file = (re.sub(r"[^a-zA-Z0-9_ ]+", "", curr_file.read().lower())).split()
                    while(read_from_file):
                        for r in read_from_file: # for every word in this line of the file
                            try: # see if this term already exists in the dictionary
                                inverted_index[r]
                            except KeyError: # create new entry for the term
                                inverted_index[r] = IndexEntry()

                            try: # see if a posting list entry for this document exists in this term's index entry
                                inverted_index[r].posting_list[current_docID]
                            except KeyError:
                                inverted_index[r].posting_list[current_docID] = 0 # create the posting list entry and initialize the TF as zero
                                inverted_index[r].docID_list.append(current_docID) # this is a new document

                            inverted_index[r].term = r
                            inverted_index[r].posting_list[current_docID] += 1 # increment the TF for this posting list entry
                            inverted_index[r].term_tf += 1 # Note: this is the sum of the posting list entries' TF values

                        read_from_file = (re.sub(r"[^a-zA-Z0-9_ ]+", "", curr_file.read().lower())).split()
                    current_docID += 1

        inverted_index = OrderedDict(sorted(inverted_index.items(), key=lambda t: t[0])) # sort the inverted index

        """ OUTPUT FOR DEBUGGING
        for term, index in inverted_index.items():
            print(end="" "{ %s , %s , %s } \t\t -> " % (index.term, len(index.docID_list), index.term_tf) )
            first = True
            for docID, TF in index.posting_list.items():
                if not first:
                    print(end="" " -> ")
                print(end="" "[%s | %s]" % (docID, TF))
                first = False
            print("")
        """


    except Exception as e:
        raise
