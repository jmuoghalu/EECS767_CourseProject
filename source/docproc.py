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
        self.in_script = self.in_cite = self.in_span = False
        self.convert_charrefs = True
        self.stemmer = PorterStemmer()

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.in_script = True
        elif tag == "span":
            self.in_span = True
        elif tag == "cite":
            self.in_cite = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False
        elif tag == "span":
            self.in_span = False
        elif tag == "cite":
            self.in_cite = False

    def handle_data(self, data):
        if (not self.in_script) and (not self.in_cite) and (not self.in_span):
            data_list = (re_sub(r"[^a-zA-Z0-9_ ]+", "", data.lower().strip())).split()
                # re.sub = remove non alphanumeric characters from the string; NOTE: this alters the format of hyperlinks
            rm_dl_stopwords = [dl for dl in data_list if dl not in stopwords.words("english")]
            stemmed_list = [self.stemmer.stem(dl) for dl in rm_dl_stopwords]

            if len(stemmed_list) > 0:
                for sl in stemmed_list:
                    self.out_file.write(sl + " ")


    def runDocProc(self, in_file_location):
        try:
            # in_file_location is a folder within the file_cache/unprocessed/
            proc_location = ""

            if not in_file_location[len(in_file_location)-1] == '/':
                in_file_location += "/"

            if not os.path.exists(in_file_location):
                print("The Input Directory Does Not Exist")
                return proc_location

            for root, dirs, files in os.walk(in_file_location):
                proc_location = "../file_cache/processed/" + os.path.basename(os.path.dirname(root)) + "/"
                print("proc_location: %s" % proc_location)
                if not os.path.exists(proc_location):
                    os.makedirs(proc_location)

                for f in files:
                    out_name = ""
                    for i in range(0, len(f)):
                        if f[i] == '.':
                            break
                        out_name += f[i]

                    curr_file = open((in_file_location + f), "r", encoding="UTF8")
                    self.out_file = open((proc_location + out_name + ".txt"), "w", encoding="UTF8")

                    read_from_file = curr_file.readline()
                    while(read_from_file):
                        self.feed(read_from_file)
                        read_from_file = curr_file.readline() # the docsnew files have each tag written in one line

                    curr_file.close()
                    self.out_file.close()

            return proc_location

        except Exception as e:
            raise
