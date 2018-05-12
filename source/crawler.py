# -*- coding: utf-8 -*-

import sys, math
from spider import mySpider

def print_usage():
    print ("\n------------------------- How to call ------------------------\n"
           "Option 1. Crawl entire desired website:\n"
           "          python crawler.py [target website]\n"
           "Option 2. Crawl max pages on website:\n"
           "          python crawler.py [target website] [number pages]\n"
           "--------------------------------------------------------------\n")


def main():
    # Set arguments
    args = sys.argv[1:]

    # Check how to crawl decision
    if len(args) == 1:
        url = args[0]
        print "Started crawling " + url + " domain"
        spider = mySpider()
        spider.crawl(url, float('inf'))
        print "Finished crawling " + url
    elif len(args) == 2:
        url = args[0]
        maxFiles = int(args[1])
        print "Started crawling " + url + " domain"
        spider = mySpider()
        spider.crawl(url, maxFiles)
        print "Finished crawling " + url
    else:
        print_usage()


if __name__ == "__main__":
    main()
