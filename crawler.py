#!/usr/bin/env python

import commands
import re
from location import loc
from optparse import OptionParser

def main():
    (options, args) = parser.parse_args()
    statout = commands.getstatusoutput('ls '+options.s+' > '+options.f)
    users = open(options.f,'r')         #user listing
    ofile = open(options.o,'w')         #output file
    numusers = 0                        #number of users
    locusers = 0                        #number of users with location
    coordusers = 0                      #number of users with coordinates
    for line in users: #for each user in listing
        numusers += 1
        user = options.s+line[0:-1] #absolute path to user page
        username = user[user.rfind('/')+1:user.rfind('.')] #isolate username
        if options.v: #verbose option
            print "username: ",username
        page = open(user,'r')
        contents = page.read()          #user page contents (html)
        page.close()
        location = loc(contents)        #user location
        c = re.compile("\d{1,3}\.\d{2,6}, ?-?\d{1,3}\.\d{2,6}")
        if options.v: #verbose option
            print location, "\n"
        if location: #location specified
            coord = c.match(location)   #match coordinates
            if coord: #location includes coordinates
                coordinates = location[coord.start():coord.end()]
                ofile.write(username+': '+coordinates+'\n')
                coordusers += 1
            else:
                ofile.write(username+': '+location+'\n')
            locusers += 1
    percent = float(locusers)/float(numusers)   # % users with location 
    pcoord = float(coordusers)/float(numusers)  # % users with coordinates
    plcoord = float(coordusers)/float(locusers) # % locations that have coordinates
    if options.v: #verbose option
        print "number of users: ",numusers
        print "number of users with location: ",locusers
        print "percentage users with location: ",percent
        print "number of users with coordinates: ",coordusers
        print "percentage users with coordinates: ",pcoord
        print "percentage location users with coordinates: ",plcoord
    ofile.write("\n\nnumber of users: "+str(numusers))
    ofile.write("\nnumber of users with location: "+str(locusers))
    ofile.write("\npercentage users with location: "+str(percent))
    ofile.write("\nnumber of users with coordinates: "+str(coordusers))
    ofile.write("\npercentage users with coordinates: "+str(pcoord))
    ofile.write("\npercentage location users with coordinates: "+str(plcoord))
    ofile.close()
    users.close()

parser = OptionParser()
#verbose
parser.add_option(
    "-v",
    "--verbose",
    action="store_true",
    dest="v",
    default=False,
    help="turn on verbose mode" )
#directory with user pages
parser.add_option("-s",
    "--source",
    dest="s",
    metavar="DIR",
    default="/project/wdim/crawlData/good_sample/",
    help="directory to find user pages in" )
#file for user listing
parser.add_option("-f",
    "--file",
    dest="f",
    metavar="FILE",
    default="users.txt",
    help="file to write user page names to")
#output file
parser.add_option("-o",
    "--outfile",
    dest="o",
    metavar="OUTPUT_FILE",
    default="cData.txt",
    help="file to write output of location data extracted by crawl")

if __name__ == "__main__":
    main()
