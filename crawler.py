#!/usr/bin/env python

import commands
from jk_loc import loc
#from BeautifulSoup import BeautifulSoup
#import re
from optparse import OptionParser

def main():
    (options, args) = parser.parse_args()
    statout = commands.getstatusoutput('ls '+options.s+' > '+options.f)
    users = open(options.f,'r')
    for line in users:
        user = options.s+line[0:-1]
        print "user: ",user
        page = open(user,'r')
        contents = page.read()
        page.close()
        location = loc(contents)
        print location, "\n"
    users.close()

parser = OptionParser()
parser.add_option(
    "-v",
    "--verbose",
    action="store_true",
    dest="v",
    default=False,
    help="turn on verbose mode" )
parser.add_option("-s",
    "--source",
    dest="s",
    metavar="DIR",
    default="/project/wdim/crawlData/good_sample/",
    help="directory to find user pages in" )
parser.add_option("-f", "--file", dest="f", metavar="FILE", default="users.txt", help="file to write user page names to")

if __name__ == "__main__":
    main()
