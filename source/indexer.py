import math, os
from collections import OrderedDict
from re import sub as re_sub, search as re_search

class InvertedIndex:
    def __init__(self):
        self.inverted_index = {} # {term: IndexEntry}
        self.document_list = [] # [[docName, docID]] # using a list instead of a dictionary to preserve ordering by docID
        self.document_lengths = []  #  ordered by docID

    class IndexEntry:
        def __init__(self):
            self.term = ""
            self.term_idf = 0
            self.term_df = 0
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
                    self.document_list.append([(os.path.splitext(f)[0]), current_docID])
                    # does not drop the file extension
                    #self.document_list.append([f, current_docID])

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
                                self.inverted_index[r].term_df += 1 # this is a new document

                            self.inverted_index[r].term = r
                            self.inverted_index[r].posting_list[current_docID] += 1 # increment the TF for this posting list entry
                            self.inverted_index[r].term_tf += 1 # Note: this is the sum of the posting list entries' TF values

                        read_from_file = (re_sub(r"[^a-zA-Z0-9_ ]+", "", curr_file.read().lower())).split()
                    curr_file.close()
                    current_docID += 1

            # set all term IDF's
            for entry in self.inverted_index.values():
                entry.term_idf = float("{0:.3f}".format(math.log10( len(self.document_list) / entry.term_df )))

            self.inverted_index = OrderedDict(sorted(self.inverted_index.items(), key=lambda t: t[0])) # sort the inverted index


            # save the inverted index to a text file
            iid_file_name = "../data/" + os.path.basename(os.path.dirname(proc_doc_location)) + "_index.txt"
            iid_file = open(iid_file_name, "w", encoding="UTF8")
            self.document_lengths = [0 for i in range(len(self.document_list))]

            iid_file.write("BEGIN TERMS\n\n")
            for term, entry in self.inverted_index.items():
                iid_file.write(
                    "Term:\t{0}\n\tDF:\t{1}\t|||\tTF:\t{2}\t|||\tIDF:\t{3}\n".format(
                    term, entry.term_df, entry.term_tf, entry.term_idf)
                )
                iid_file.write("\tPosting List: (docID,docTF)\n")
                #iid_file.write("\tPosting List: (first line = docID,docTF; second line = docTFIDFweight)\n")

                docIDandTF_line = ""
                #weight_line = ""
                for docID, TF in entry.posting_list.items():
                    self.document_lengths[docID-1] += (entry.term_idf*TF)*(entry.term_idf*TF)
                    docIDandTF_line += "{0},{1}\t\t".format(docID,TF)
                    #weight_line += "{0}\t\t".format(entry.term_idf*TF)
                #iid_file.write("\t\t{0}\n\t\t{1}\n\n\n".format(docIDandTF_line, weight_line))
                iid_file.write("\t\t{0}\n\n\n".format(docIDandTF_line))

            iid_file.write("\nEND TERMS\n\n\nBEGIN DOCUMENTS\n\n\n")
            for docInfo in self.document_list: # [[docName, docID]]:
                self.document_lengths[docInfo[1]-1] = float("{0:.3f}".format(math.sqrt(self.document_lengths[docInfo[1]-1])))
                iid_file.write("D{0}:\t{1}\n\tLength:\t{2}\n\n".format(docInfo[1], docInfo[0], self.document_lengths[docInfo[1]-1]))
            iid_file.write("\nEND DOCUMENTS")

            iid_file.close()


        except Exception as e:
            raise


    # after calling createInvertedIndex, the inverted index has now been sorted and written to file
    def loadInvertedIndex(self, proc_doc_location):
        if not proc_doc_location[len(proc_doc_location)-1] == '/':
            proc_doc_location += "/"

        if not os.path.exists(proc_doc_location):
            print("The Input Directory Does Not Exist")
            return

        iid_file_name = "../data/" + os.path.basename(os.path.dirname(proc_doc_location)) + "_index.txt"
        if not os.path.isfile(iid_file_name):
            self.createInvertedIndex(proc_doc_location)
        else:
            self.inverted_index = {}
            self.document_list = []
            file = open(iid_file_name, encoding="UTF8")
            reading_terms = reading_docs = False

            read_from_file = file.readline()
            while(read_from_file):
                if read_from_file == "\n" or read_from_file == "":
                    read_from_file = file.readline()
                    continue
                elif read_from_file.startswith("BEGIN TERMS"):
                    reading_terms = True; reading_docs = False
                elif read_from_file.startswith("END TERMS"):
                    reading_terms = False;
                elif read_from_file.startswith("BEGIN DOCUMENTS"):
                    reading_terms = False; reading_docs = True
                elif read_from_file.startswith("END DOCUMENTS"):
                    reading_docs = False
                else:
                    if reading_terms:
                        if read_from_file.startswith("Term:"):
                            term = read_from_file.strip().split(":\t")[1]
                            try:
                                self.inverted_index[term]
                            except KeyError:
                                self.inverted_index[term] = self.IndexEntry()
                            self.inverted_index[term].term = term

                            read_from_file = file.readline().strip()
                            values = read_from_file.split("|||")
                            self.inverted_index[term].term_df = int(values[0].strip().split(":\t")[1])
                            self.inverted_index[term].term_tf = int(values[1].strip().split(":\t")[1])
                            self.inverted_index[term].term_idf = float(values[2].strip().split(":\t")[1])

                            file.readline()
                            read_from_file = file.readline().strip()
                            posting_list_items = read_from_file.split("\t\t")
                            for it in posting_list_items:
                                it_items = it.split(",")
                                self.inverted_index[term].posting_list[int(it_items[0])] = int(it_items[1])

                    elif reading_docs:
                        if read_from_file.startswith("D"):
                            rff = read_from_file.strip().split(":\t")
                            docName = rff[1]
                            docID = int(rff[0].split("D")[1])
                            self.document_list.append([docName, docID])

                            read_from_file = file.readline().strip()
                            docLen = float(read_from_file.split(":\t")[1])
                            self.document_lengths.append(docLen)


                read_from_file = file.readline()

            file.close()
            self.inverted_index = OrderedDict(sorted(self.inverted_index.items(), key=lambda t: t[0])) # sort the inverted index
