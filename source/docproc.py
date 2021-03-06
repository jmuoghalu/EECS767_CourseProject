import sys
sys.path.append("/nltk-3.3/")
sys.path.append("/home/j286m692/EECS_767/EECS767_CourseProject/source/nltk-3.3/")
sys.path.append("/home/j286m692/nltk_data/")
import os
from html.parser import HTMLParser
from html.entities import name2codepoint
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from re import sub as re_sub

class DocProcessor(HTMLParser):

    def __init__(self):
        super().__init__()
        self.reset()
        self.out_file = None
        self.in_title = self.in_body = self.in_para = self.in_script = self.in_cite = self.in_span = False # flags for HTML parsing
        self.convert_charrefs = True
        self.current_doc_title = self.current_line = "" # helper variables for displaying search results
        self.not_in_processing = False
        self.stemmer = PorterStemmer()

        # get the stopwords for document processing
        english_file = open("./nltk-3.3/nltk_data/corpora/stopwords/english", "r", encoding="UTF8")
        self.english_words = english_file.read().strip().split()
        english_file.close()

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        elif tag == "body":
            self.in_body = True
        elif tag == "p":
            self.in_para = True
        elif tag == "script":
            self.in_script = True
        elif tag == "span":
            self.in_span = True
        elif tag == "cite":
            self.in_cite = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "body":
            self.in_body = False
        elif tag == "p":
            self.in_para = False
        elif tag == "script":
            self.in_script = False
        elif tag == "span":
            self.in_span = False
        elif tag == "cite":
            self.in_cite = False

    def handle_data(self, data):
        # getting the name of a document result
        if self.in_title and self.not_in_processing:
            self.current_doc_title = data.strip() + " "

        # getting the snapshot of a document result
        elif (not self.in_script) and (not self.in_title) and self.in_para and self.not_in_processing:
            if len(data.strip()) > 1:
                self.current_line += data.strip() + " "

        # HTML document processing
        elif (not self.in_script) and (not self.in_cite) and (not self.in_span) and (not self.not_in_processing):
            data_list = (re_sub(r"[^a-zA-Z0-9_ ]+", "", data.lower().strip())).split()
                # re.sub = remove non alphanumeric characters from the string; NOTE: this alters the format of hyperlinks

            # do not add raw numbers to the token stream
            rm_dl_stopwords = [dl for dl in data_list if (dl not in self.english_words) and (not dl.isdigit())]
            stemmed_list = [self.stemmer.stem(dl) for dl in rm_dl_stopwords]

            if len(stemmed_list) > 0:
                for sl in stemmed_list:
                    self.out_file.write(sl + " ")


    def runDocProc(self, in_file_location):
        self.not_in_processing = False
        try:
            # in_file_location is a folder within the file_cache/unprocessed/ directory
            proc_location = ""

            # error checking and formatting of the directory location
            if not in_file_location[len(in_file_location)-1] == '/':
                in_file_location += "/"
            if not os.path.exists(in_file_location):
                return ("The Input Directory Does Not Exist")

            for root, dirs, files in os.walk(in_file_location):
                proc_location = "../file_cache/processed/" + os.path.basename(os.path.dirname(root)) + "/"
                if not os.path.exists(proc_location):
                    os.makedirs(proc_location)

                # the processed version of this file will be a .txt file with the same name
                for f in files:
                    out_name = ""
                    for i in range(0, len(f)):
                        if f[i] == '.':
                            break
                        out_name += f[i]

                    # process the file
                    curr_file = open((in_file_location + f), "r", encoding="UTF8")
                    self.out_file = open((proc_location + out_name + ".txt"), "w", encoding="UTF8")
                    self.feed(curr_file.read())
                    curr_file.close()
                    self.out_file.close()

            return proc_location

        except Exception as e:
            raise()


    def retrieveDocTitle(self, full_file_name):
        file = open(full_file_name, "r", encoding="UTF8")
        try:
            self.not_in_processing = True
            self.current_doc_title = ""
            ret = ""
            for read_from_file in file:
                # read the HTML file until the title has been retrieved
                self.feed(read_from_file.strip())
                if not (self.current_doc_title == ""):
                    ret = self.current_doc_title
                    break
            file.close()
            self.in_title = self.in_body = self.in_para = self.in_script = self.in_cite = self.in_span = False
            return ret
        except Exception as e:
            file.close()


    def retrieveDocSnapshot(self, full_file_name, query_terms):
        file = open(full_file_name, "r", encoding="UTF8")
        try:
            self.not_in_processing = True
            ret = ""

            # read the HTML file until the first paragraph has been retrieved, which will serve as the snapshot
            for read_from_file in file:
                self.feed(read_from_file.strip())

                if not (self.current_line == ""):
                    rm_internal_tags = re_sub(r"[<.*>]+", "", self.current_line.lower().strip())
                    line_list_of_words = re_sub(r"[^a-zA-Z0-9_ ]+", "", rm_internal_tags).split()
                    rm_llw_stopwords = [lw for lw in line_list_of_words if lw not in self.english_words]
                    stem_llw = [self.stemmer.stem(lw) for lw in rm_llw_stopwords]

                    # check for any shared elements between the query and this line in the file
                    # if there are shared elements, then this is a valid snapshot
                    ret = self.current_line
                    #if not (set(stem_llw).isdisjoint(query_terms)):
                    if not self.in_para:
                        break

            self.current_line = ""
            self.in_title = self.in_body = self.in_para = self.in_script = self.in_cite = self.in_span = False
            file.close()
            return ret
        except Exception as e:
            file.close()
