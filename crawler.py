#!/usr/bin/env python

import sys
import commands
import re
from location import loc,ltweet
from optparse import OptionParser

def main():
    (options, args) = parser.parse_args()
    statout = commands.getstatusoutput('ls '+options.d+' > '+options.f)
    users = open(options.f,'r')         #user listing
    out = open(options.o,'w')           #output file
    if options.s: #if no output file
        out = sys.stdout #print to stdout
    numusers = 0.0                      #number of users
    locusers = 0.0                      #number of users with location
    coordusers = 0.0                    #number of users with coordinates
    twtusers = 0.0                      #number of users using l:____
    for line in users: #for each user in listing
        numusers += 1
        user = options.d+line[0:-1] #absolute path to user page
        username = user[user.rfind('/')+1:user.rfind('.')] #isolate username
        if options.v: #verbose option
            print >>out,"username: ",username
        page = open(user,'r')
        contents = page.read()          #user page contents (html)
        page.close()
        location = loc(contents)        #user location
        c = re.compile("\d{1,3}\.\d{2,6}, ?-?\d{1,3}\.\d{2,6}")
        if options.v: #verbose option
            print >>out,location
        if location: #location specified
            coord = c.match(location)   #match coordinates
            if coord: #location includes coordinates
                coordinates = location[coord.start():coord.end()]
                print >>out,username,': ',coordinates
                coordusers += 1
            else:
                print >>out,username,': ',location
            locusers += 1
        tweets = ltweet(contents)
        if tweets: #l:___ found
            print >>out,str(tweets)
            twtusers += 1
    percent = locusers/numusers         # % users with location 
    pcoord = coordusers/numusers        # % users with coordinates
    plcoord = coordusers/locusers       # % locations that have coordinates
    ptweet = twtusers/numusers          # % users using l:____
    print >>out,"\n"
    print >>out,"number of users: %d" % numusers
    print >>out,"number of users with location: %d" % locusers
    print >>out,"percentage users with location: %f" % percent
    print >>out,"number of users with coordinates: %d" % coordusers
    print >>out,"percentage users with coordinates: %f" % pcoord
    print >>out,"percentage location users with coordinates: %f" % plcoord
    print >>out,"number of users using l:____: %d" % twtusers
    print >>out,"percentage users using l:____: %f" % ptweet
    users.close()

parser = OptionParser()
parser.add_option(                      #verbose
    "-v",
    "--verbose",
    action="store_true",
    dest="v",
    default=False,
    help="turn on verbose mode" )
parser.add_option(                      #directory with user pages
    "-d",
    "--directory",
    dest="d",
    metavar="DIR",
    default="/project/wdim/crawlData/good_sample/",
    help="directory to find user pages in" )
parser.add_option(                      #file for user listing
    "-f",
    "--file",
    dest="f",
    metavar="FILE",
    default="users.txt",
    help="file to write user page names to")
parser.add_option(                      #use stdout for output
    "-s",
    "--stdout",
    action="store_true",
    dest="s",
    default=False,
    help="use standard output instead of output file")
parser.add_option(                      #output file
    "-o",
    "--outfile",
    dest="o",
    metavar="OUTPUT_FILE",
    default="cData.txt",
    help="file to write output of location data extracted by crawl")

if __name__ == "__main__":
    main()
