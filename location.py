#!/usr/bin/env python

import urllib
import re
from optparse import OptionParser

def main():
    (options, args) = parser.parse_args()
  
    if options.v:
        print "verbose mode on"
    if options.f:
        if options.v:
            print "input file: ", options.f
        file = open(options.f,'r')
        contents = file.read()
        file.close()
        print "contents of file: ",contents
#        l = re.compile("(?i)l:\w+|<span class=\"adr\">[\w, -\.:]+</span>|iphone: \d{1,2}\.\d{6},-?\d{1,2}\.\d{6}")
#        result = l.findall(contents)
#        print result
        a = re.compile("(?i)<span class=\"adr\">[\w, -\.:]+</span>")
        loc = str(a.findall(contents))
        print loc[loc.find(">")+1:loc.rfind("<")]

parser = OptionParser()
parser.add_option("-v", "--verbose", action="store_true", dest="v", default=False, help="turn on verbose mode")
parser.add_option("-f", "--file", dest="f", metavar="FILE", help="name of input file to search")
        
if __name__ == "__main__":
    main()
