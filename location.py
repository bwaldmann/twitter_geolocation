#!/usr/bin/env python

import sys
import re
from optparse import OptionParser

def loc(contents):
    a = re.compile("<span class=\"adr\">([\w, -\.:]+)</span>",re.I)
    loc = a.search(contents)
    coordinates = False
    if loc: #location specified
        location = contents[loc.start():loc.end()] #isolate location
        location = location[location.find(">")+1:location.rfind("<")]
        c = re.compile("\d{1,3}\.\d{2,6}, ?-?\d{1,3}\.\d{2,6}")
        coord = c.search(location)
        if coord: #coordinates specified
            coordinates = location[coord.start():coord.end()]
    else:
        location = False
    return [location,coordinates]

def ltweet(contents):
    l = re.compile("l:(\w+)",re.I)
    tweet = l.findall(contents)
    return tweet

def main():
    (options, args) = parser.parse_args()
    out = open(options.f,'w')
    if options.s:
        out = sys.stdout
    if options.v: #verbose option
        print >>out,"verbose mode on"
        print >>out,"input file: %s" % options.f
    file = open(options.f,'r')
    contents = file.read()              #contents of input file
    file.close()
    location = loc(contents)            #address
    if options.v: #verbose option
        print >>out,"contents of file: %s" % contents
    print >>out,location
    tweets = ltweet(contents)
    if tweets: #tweets contain l:____ refs
        print >>out,"%s" % tweets

parser = OptionParser()
parser.add_option(                      #input file
    "-f",
    "--file",
    dest="f",
    default="infile.html",
    metavar="FILE",
    help="input file to search")
parser.add_option(                      #output file
    "-o",
    "--outfile",
    dest="o",
    default="lData.txt",
    metavar="OUTPUT_FILE",
    help="file to write output of location search")
parser.add_option(                      #use stdout for output
    "-s",
    "--stdout",
    action="store_true",
    dest="s",
    default=False,
    help="use standard output instead of output file")
parser.add_option(                      #verbose
    "-v",
    "--verbose",
    action="store_true",
    dest="v",
    default=False,
    help="turn on verbose mode")
        
if __name__ == "__main__":
    main()
