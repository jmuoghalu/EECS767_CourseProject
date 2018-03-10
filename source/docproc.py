import math, os, sys
from html.parser import HTMLParser
from html.entities import name2codepoint

class DocProcessor(HTMLParser):

    def __init__(self):
        super().__init__()
        self.reset()
        self.out_file = None
        self.in_script = self.in_cite = self.in_span = False
        self.convert_charrefs = True

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
            self.out_file.write(data.lower())




if __name__ == '__main__':
    try:
        dp = DocProcessor()
        in_file_name = "../docsnew/Arches_National_Park.htm"
        test_file = open(in_file_name, "r")

        out_name = ""
        for i in range(11, len(in_file_name)):
            if in_file_name[i] == '.':
                break
            out_name += in_file_name[i]
        dp.out_file = open("../processed_docsnew/" + out_name + ".txt", "w")
        dp.out_file.write("<!DOCTYPE html>")

        # the docsnew files have each tag written in one line
        read_from_file = test_file.readline()
        while(read_from_file):
            dp.feed(read_from_file)
            read_from_file = test_file.readline()


    except Exception as e:
        raise
