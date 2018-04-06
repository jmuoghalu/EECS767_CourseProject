import math, os, re, sys
from indexer import InvertedIndex as InvertedIndexClass

class VectorSpaceModel:
    def __init__(self, iic: InvertedIndexClass):
        self.column_headers = ["term", "IDF"] + iic.document_list

        # initialize each row with the term and the IDF value which are the first two indices
        self.term_rows = [
                [
                    term,
                    float("{0:.3f}".format(math.log10( len(iic.document_list) / len(entry.docID_list) ))),
                ] +
                [
                    0 for i in range(0, len(iic.document_list))
                ]
            for term, entry in iic.inverted_index.items()
        ]
        for row in self.term_rows: # fill the tf-idf weights for each term
            entry = iic.inverted_index[row[0]]
            for docID, TF in entry.posting_list.items():
                row[2 + (docID-1)] = row[1] * TF

        self.document_vectors = []

    def document_lengths(self, document_index):
        v = [row[document_index] for row in self.term_rows]
        length = 0
        for x in v:
            length += (x * x)
        return float("{0:.3f}".format(math.sqrt(length)))


def debugPrint(vsm,iic):

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

    print("\n\n")

    for x in vsm.column_headers:
        print(x + "\t\t", end='')
    print()

    for row in vsm.term_rows:
        if len(row[0]) < 8:
            print(row[0] + "\t\t", end='')
        else:
            print(row[0] + "\t", end='')

        for val in row[1:]:
            print(str(val) + "\t\t", end='')
        print()

    print("\nDocument Lengths\n\t\t\t\t", end='')
    for x in range(2, len(vsm.column_headers)):
        print(str(vsm.document_lengths(x)) + "\t\t", end='')



if __name__ == "__main__":
    try:
        proc_doc_location = "../testdoc"
        iic = InvertedIndexClass()
        iic.createInvertedIndex(proc_doc_location)
        vsm = VectorSpaceModel(iic)
        root, dirs, files = os.walk(proc_doc_location).__next__()

        debugPrint(vsm, iic)



    except Exception as e:
        raise

    """
    To implement the stemmer and stopper, Python provides easily available stemmers and stoppers libraries that can be imported, created by the Natural Language Toolkit (NLTK). Each processed file is output to a new corresponding processed file. Once the file has been processed, each word is added to the dictionary array as a tuple containing the word and its document frequency, with a pointer to the posting list object that contains the document number, frequency, and a pointer to the next object, creating a linked list. After document preprocessing is done, the dictionary data is used to calculate the TF-IDF based ranking for each document. We are currently working on comparing the query and document vectors efficiently, and determining which data structures would be most beneficial to hold the vectors and inverted index.
    """
