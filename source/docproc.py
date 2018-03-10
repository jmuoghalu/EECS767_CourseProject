import math, os, sys
from HTMLParser import HTMLParser

class DocProcessor(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.in_body = False
        self.out_file = None

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.in_body = True

        self.out_file.write("<" + tag)
        for x in attrs:
            self.out_file.write(" " + str(x[0]) + "=\"" + str(x[1]) + "\"")
        self.out_file.write(">")

    def handle_endtag(self, tag):
        self.out_file.write("</" + tag + ">")

    def handle_data(self, data):
        self.out_file.write(data)



if __name__ == '__main__':
    try:
        dp = DocProcessor()
        in_file_name = "../docsnew/Arches_National_Park.htm"
        test_file = open(in_file_name, "r")

        out_name = ""
        for i in range(11, len(in_file_name)):
            out_name += in_file_name[i]
        dp.out_file = open("../processed_docsnew/" + out_name, "w")
        dp.out_file.write("<!DOCTYPE html>")

        # the docsnew files have each tag written in one line
        read_from_file = test_file.readline()
        while(read_from_file):
            if read_from_file[len(read_from_file)-1] == '\n':
                dp.feed(read_from_file)
                read_from_file = test_file.readline()
            else:
                dp.feed(read_from_file)
                print "End of File\n"
                break

    except Exception as e:
        raise
