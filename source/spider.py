# -*- coding: utf-8 -*-

import os, re, urllib, urllib.request, urllib.parse, urllib.robotparser
from html.parser import HTMLParser
from urllib.parse import urljoin as urljoinFun
from urllib.request import urlopen as urlopenFun

# Trying to figure out certification errors on some sites
hdr = {'User-Agent':'Mozilla/5.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

class HTMLParser(HTMLParser):

    # overrides the handle_starttag(tag, attrs) function of HTMLParser from python library
    def handle_starttag(self, tag, attrs):
        for link, path in attrs:
            if link == "href":
                if re.match(r'^.*\.(css|gif|jpeg|jpg|js|pdf|png|ico|rss|txt|xml).*$', path, re.M|re.I):     # not hyperlinks
                    # print "\t", path                  # show the static file
                    # do nothing for now
                    pass
                elif tag == "a":                    # identify links
                    url = urljoinFun(self.url, path)    # append relative path to the root path

                    # standardize url so they don't end in '/', get rid of '#', and all start with http://
                    redundant = url.find('#')
                    if redundant != -1:
                        url = url[:redundant]

                    length = len(url)
                    if url[length - 1] == '/':
                        url = url[:(length - 1)]

                    if url[0:4] != "http":
                        url = "http://" + url

                    if re.match(r'^https?://([\w-]*\.)?' + self.domain + r'.*$', url, re.M|re.I):
                        self.hyperlinks.append(url)       # append url to the return list
                else:
                    pass


    def findLinks(self, url):
        # Parse the URL to get links
        self.url = url
        self.domain = "{uri.netloc}".format(uri=urllib.parse.urlparse(url))   # get domain of website

        self.hyperlinks = []                  # init return list

        try:
            openedURL = urlopenFun(url)
            html = openedURL.read().decode("utf-8") # want unicode for best parser results
            self.feed(html)
        except KeyboardInterrupt:                   # be able to handle Ctrl-C if problem occurs or want to stop early
            exit()
        except:
            print ("Some error occured.")

        return self.hyperlinks #returns links from url


class mySpider(object):
    def __init__(self):
        self.will_crawl = []
        self.visted = set([])
        self.parser = HTMLParser()

    def crawl(self, initial_url, maxFiles):
        # standardize url so that it doesn't end in '/', get rid of '#', and starts with http://
        redundant = initial_url.find('#')
        if redundant != -1:
            initial_url = initial_url[:redundant]

        length = len(initial_url)
        if initial_url[length - 1] == '/':
            initial_url = initial_url[:(length - 1)]

        if initial_url[0:4] != "http":
            initial_url = "http://" + initial_url

        # Add in check for robots.txt to insure it is polite
        initdomain = "{uri.netloc}".format(uri=urllib.parse.urlparse(initial_url))
        print ("domain is " + initdomain)
        robot = urllib.robotparser.RobotFileParser()
        robot.set_url("http://" + initdomain + "/robots.txt")
        print ("check 1")
        robot.read()
        print ("check 2")
        if (robot.can_fetch("*", initial_url)):
            self.will_crawl.append(initial_url)    # put initial_url to will_crawl list if allowed

        filenum = 1                         # initialize number of files downloaded
        directory = "../file_cache/unprocessed/newly_crawled/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        while (len(self.will_crawl) > 0) and (filenum <= maxFiles):

            url = self.will_crawl.pop(0)      # get next url
            try:
                print ("Spider at:", url)
                openedURL = urlopenFun(url)
                sourceCode = openedURL.read()
                encoded = urllib.parse.quote(str(url), safe='.')      # encode URL so it can be a file name
                encoded = encoded.replace(".", "%2E")

                try:
                    name = '{0}/{1}.html'.format(directory, encoded)
                    f = open(name, 'wb')
                    f.write(sourceCode)
                    filenum = filenum + 1           # keeps track of files downloaded if needed
                    f.close()
                except:
                    print ("\tFile Exception\t{0}".format(name))

                links = self.parser.findLinks(url)    # parse url
                self.visted.add(url)            # mark url as visted

                # Add links to will_crawl list if not visited already and if robots.txt says is polite
                for url in links:
                    # print (robot.can_fetch("*", url))
                    try:
                        if (url not in self.visted) and (url not in self.will_crawl) and (robot.can_fetch("*", url)):
                            self.will_crawl.append(url)
                    except:
                        self.visted.add(url)
                        print ("Some error occurred adding to frontier.")
            except Exception as e:
                self.visted.add(url)
                print(e)
