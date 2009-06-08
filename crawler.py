#!/usr/bin/env python

import commands
from location import loc
from optparse import OptionParser

def main():
    (options, args) = parser.parse_args()
    statout = commands.getstatusoutput('ls '+options.s+' > '+options.f)
    users = open(options.f,'r')
    ofile = open(options.o,'w')
    numusers = 0
    locusers = 0
    for line in users:
        numusers += 1
        user = options.s+line[0:-1]
        username = user[user.rfind('/')+1:user.rfind('.')]
        if options.v:
            print "username: ",username
        page = open(user,'r')
        contents = page.read()
        page.close()
        location = loc(contents)
        if options.v:
            print location, "\n"
        if location:
            ofile.write(username+': '+location+'\n')
            locusers += 1
    percent = float(locusers)/float(numusers)
    if options.v:
        print "number of users: ",numusers
        print "number of users with location: ",locusers
        print "percentage users with location: ",percent
    ofile.write("\n\nnumber of users: "+str(numusers))
    ofile.write("\nnumber of users with location: "+str(locusers))
    ofile.write("\npercentage users with location: "+str(percent))
    ofile.close()
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
parser.add_option("-f",
    "--file",
    dest="f",
    metavar="FILE",
    default="users.txt",
    help="file to write user page names to")
parser.add_option("-o",
    "--outfile",
    dest="o",
    metavar="OUTPUT_FILE",
    default="output.txt",
    help="file to write output of location data extracted by crawl")

if __name__ == "__main__":
    main()
