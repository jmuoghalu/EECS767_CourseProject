import math, os
from collections import OrderedDict
from re import sub as re_sub

class InvertedIndex:
    def __init__(self):
        self.inverted_index = {} # {term: IndexEntry}
        self.document_list = [] # [[docName, docID]] # using a list instead of a dictionary to preserve ordering by docID

    class IndexEntry:
        def __init__(self):
            self.term = ""
            self.term_idf = 0
            self.docID_list = [] # the size of this list is the term's DF
            self.term_tf = 0
            self.posting_list = {} # [docID: docTF]


    def createInvertedIndex(self, proc_doc_location):
        try:
            self.inverted_index = {}
            self.document_list = []
            current_docID = 1

            if not proc_doc_location[len(proc_doc_location)-1] == '/':
                proc_doc_location += "/"

            if not os.path.exists(proc_doc_location):
                print("The Input Directory Does Not Exist")
                return

            """
            build the unsorted inverted index
            if a term appears in multiple documents, the DocIDs will be saved as a list
                self.inverted_index = { term : IndexEntry }
                IndexEntry.posting_list = { docID : TF }
            """
            for root, dirs, files in os.walk(proc_doc_location):
                for f in files:
                    # drops the file extension
                    #self.document_list.append([(os.path.splitext(f)[0]), current_docID])
                    # does not drop the file extension
                    self.document_list.append([f, current_docID])
                    curr_file = open((proc_doc_location + f), "r", encoding="UTF8")

                    # read a line; convert to lowercase; remove punctuation, and separate the words
                    read_from_file = (re_sub(r"[^a-zA-Z0-9_ ]+", "", curr_file.read().lower())).split()
                    while(read_from_file):
                        for r in read_from_file: # for every word in this line of the file
                            try: # see if this term already exists in the dictionary
                                self.inverted_index[r]
                            except KeyError: # create new entry for the term
                                self.inverted_index[r] = self.IndexEntry()

                            try: # see if a posting list entry for this document exists in this term's index entry
                                self.inverted_index[r].posting_list[current_docID]
                            except KeyError:
                                self.inverted_index[r].posting_list[current_docID] = 0 # create the posting list entry and initialize the TF as zero
                                self.inverted_index[r].docID_list.append(current_docID) # this is a new document

                            self.inverted_index[r].term = r
                            self.inverted_index[r].posting_list[current_docID] += 1 # increment the TF for this posting list entry
                            self.inverted_index[r].term_tf += 1 # Note: this is the sum of the posting list entries' TF values

                        read_from_file = (re_sub(r"[^a-zA-Z0-9_ ]+", "", curr_file.read().lower())).split()
                    current_docID += 1

            # set all term IDF's
            for entry in self.inverted_index.values():
                entry.term_idf = float("{0:.3f}".format(math.log10( len(self.document_list) / len(entry.docID_list) )))

            self.inverted_index = OrderedDict(sorted(self.inverted_index.items(), key=lambda t: t[0])) # sort the inverted index

            iid_file_name = "../data/" + os.path.basename(os.path.dirname(proc_doc_location)) + "_index.txt"

            """ OUTPUT FOR DEBUGGING
            for term, index in self.inverted_index.items():
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
            #"""
            iid_file = open(iid_file_name, "w", encoding="UTF8")
            for docInfo in self.document_list: # [[docName, docID]]:
                iid_file.write("D%s:\t\t%s\n" % (docInfo[1], docInfo[0]))

            iid_file.write("\n\n\n")
            for term, entry in self.inverted_index.items():
                iid_file.write("Term:\t%s\n" % term)
                iid_file.write("\tDF:\t%s\n" % len(entry.docID_list))
                iid_file.write("\tTF:\t%s\n" % entry.term_tf)
                iid_file.write("\tIDF:\t%s\n" % entry.term_idf)
                #iid_file.write()
                iid_file.write("\tPosting List: (first line = docID; second line = docTF)\n")

                docID_line = ""
                postlist_line = ""
                for docID, TF in entry.posting_list.items():
                    docID_line += "{0}\t\t".format(docID)
                    postlist_line += "{0}\t\t".format(TF)
                iid_file.write("\t\t{0}\n\n\t\t{1}\n".format(docID_line, postlist_line))
                iid_file.write("\n\n")

            iid_file.close()


        except Exception as e:
            raise


    # after calling createInvertedIndex, the inverted index has now been sorted and can be written to file
    def loadInvertedIndex(self, proc_doc_location):
        if not proc_doc_location[len(proc_doc_location)-1] == '/':
            proc_doc_location += "/"

        if not os.path.exists(proc_doc_location):
            print("The Input Directory Does Not Exist")
            return

        # This function is incomplete
