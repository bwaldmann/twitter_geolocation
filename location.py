#!/usr/bin/env python

import re
from optparse import OptionParser

def loc(contents):
    a = re.compile("(?i)<span class=\"adr\">[\w, -\.:]+</span>")
    loc = a.search(contents)
    if loc: #location specified
        location = contents[loc.start():loc.end()] #isolate location
        c = re.compile("\d{1,3}\.\d{2,6}, ?-?\d{1,3}\.\d{2,6}")
        coord = c.search(location)
        #return user address
        if coord: #coordinates specified
            return location[coord.start():coord.end()]
        else: #coordinates not specified
            return location[location.find(">")+1:location.rfind("<")]

def ltweet(contents):
    l = re.compile("(?i) l:\w+")
    ltweet = l.findall(contents)
    if ltweet:
        return ltweet

def main():
    (options, args) = parser.parse_args()
    if options.v: #verbose option
        print "verbose mode on"
        print "input file: ", options.f
    file = open(options.f,'r')
    contents = file.read()              #contents of input file
    file.close()
    location = loc(contents)            #address
    if options.v: #verbose option
#        print "contents of file: ",contents
        print location
    ofile = open(options.o,'w')
    ofile.write(location) #write to output file
    ofile.close()
    #TEMPORARY
    tweets = ltweet(contents)
    if options.v: #verbose option
        print tweets

parser = OptionParser()
#verbose
parser.add_option(
    "-v",
    "--verbose",
    action="store_true",
    dest="v",
    default=False,
    help="turn on verbose mode")
#input file
parser.add_option(
    "-f",
    "--file",
    dest="f",
    default="infile.html",
    metavar="FILE",
    help="input file to search")
#use stdout for output
parser.add_option(
    "-s",
    "--stdout",
    action="store_true",
    dest="s",
    default=False,
    help="use standard output instead of output file")
#output file
parser.add_option(
    "-o",
    "--outfile",
    dest="o",
    default="lData.txt",
    metavar="OUTPUT_FILE",
    help="file to write output of location search")
        
if __name__ == "__main__":
    main()
