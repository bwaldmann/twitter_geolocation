#!/usr/bin/env python

import commands
import location
#from BeautifulSoup import BeautifulSoup
#import re
from optparse import OptionParser

def main():
    (options, args) = parser.parse_args()
    
    users = open(options.f,'w')
    users.write(commands.getoutput('ls '+options.s))
    users.close()
    
    users = open(options.f,'r')
    line = users.readline()
    while line:
        user = options.s+line[0:-1]
        print "user: ",user
        page = open(user,'r')
#        soup = BeautifulSoup(page)
#        if options.v:
#            print soup.prettify()
#        list = soup.findAll('a', attrs={'href' : re.compile("\/[\w\?=]+")})
#        if options.v:
#            print "finding location for user ", user[0:-1], ":"
#        loc = commands.getoutput('./location.py -v -f '+options.s+user)
#        print loc, "\n"
        page.close()
        line = users.readline()
    users.close()

parser = OptionParser()
parser.add_option("-v", "--verbose", action="store_true", dest="v", default=False, help="turn on verbose mode")
parser.add_option("-s", "--source", dest="s", metavar="DIR", default="/project/wdim/crawlData/good_sample/", help="directory to find user pages in")
parser.add_option("-f", "--file", dest="f", metavar="FILE", default="users.txt", help="file to write user page names to")

if __name__ == "__main__":
    main()
