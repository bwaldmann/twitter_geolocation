#!/usr/bin/env python

import sys
import commands
import re
from os import mkdir
from BeautifulSoup import BeautifulSoup
from location import loc,ltweet
import metacarta
from optparse import OptionParser
from datetime import date,datetime

def tattrs(contents,i):
    t = re.compile("<span class=\"published\" title=\"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})",re.I)
    start = contents[:i.start()].rfind("status_")+7
    end = contents[start:i.start()].find('\"')
    print "  start: %d; end: %d" % (start,end)
    id = contents[start:start+end]
    time = t.search(contents[i.end():]).group(1)
    return [id,time]
    
def meta(address):
    length = 0
    address = address
    error = False
    lat = False
    lon = False
    lf = metacarta.LocationFinder("bw1224@messiah.edu","tamuresearcher")
    lf.method = "LocationFinder"
#    print "method: %s" % lf.method
    try:
        data = lf.request({'query':address})
        length = len(data['Locations'])
        if length > 0:
            address = data['Locations'][0]['Paths']['Administrative']
            lat = data['Locations'][0]['Centroid']['Latitude']
            lon = data['Locations'][0]['Centroid']['Longitude']
    except:
        print "  error in query login!"
        error = True
    return [length,address,lat,lon,error]

def main():
    ts = 'T'.join(str(datetime.now()).split(' '))
    ts = '-'.join(ts.split(':'))
    ts = ts[:ts.rfind('.')]
    print ts
    dir = "data/%s/" % ts
    mkdir(dir)
    (options, args) = parser.parse_args()
    if options.f:
        ufile = open(options.u,'w')
        print >>ufile,options.f
        ufile.close()
    else:
        statout = commands.getstatusoutput('ls '+options.d+' > '+options.u)
    users = open(options.u,'r')         #user listing
    out = open(dir+options.o,'w') #output file
    if options.s: #if no output file
        out = sys.stdout #print to stdout
    numusers = 0.0                      #number of users
    locusers = 0.0                      #number of users with location
    coordusers = 0.0                    #number of users with coordinates
    twts = 0.0                          #number of tweets with l:____
    twtusers = 0.0                      #number of users using l:____
    vaddr = 0.0                         #number of valid addresses
    login = 0                           #number of errors logging into MC
    for line in users: #for each user in listing
        numusers += 1
        user = options.d+line[0:-1] #absolute path to user page
        username = user[user.rfind('/')+1:user.rfind('.')] #isolate username
        file = open("%s%s.txt" % (dir,username),'w')
        print username #TEMPORARY
        if options.v: #verbose option
            print >>out,username
        page = open(user,'r')
        contents = page.read()          #user page contents (html)
        page.close()
        location = loc(contents)
        if options.v: #verbose option
            print >>out,location[0]
        if location[1]: #coordinates specified
            print >>out,"%s : %s : %s" % (username,location[0],location[1])
            lat,lon = location[1].split(',')
            print >>file,"%s$xyzzy$%s$xyzzy$%s$xyzzy$%s" % (location[0],lat,lon,date.today())
            locusers += 1
            coordusers += 1
            vaddr += 1
        elif location[0]: #location (no coordinates) specified
            print >>out,"%s : %s" % (username,location[0])
            if options.m:
                set = meta(location[0])
                if set[4]: #login error
                    print >>out,"  error in query login!"
                    login += 1
                if set[0] > 0: #address(es) found
                    print "  %d addresses found" % set[0]
                    print "  address: %s" % set[1]
                    print >>out,"  %d addresses found" % set[0]
                    print >>out,"  address: %s" % set[1]
                    print >>file,"%s$xyzzy$%s$xyzzy$%s$xyzzy$%s" % (location[0],set[2],set[3],date.today())
                else: #no address found
                    print >>file,"$xyzzy$$xyzzy$$xyzzy$"
                if set[0] == 1:
                    vaddr += 1
            locusers += 1
        else: #no location specified
            print >>file,"$xyzzy$$xyzzy$"
        if options.t:
            t = re.compile("<span class=\"entry-content\">(.+?)</span>",re.I)
            s = re.compile("<span class=\"published\" title=\"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})",re.I)
            iter = t.finditer(contents)
            for i in iter:
                twtFlag = False                     #user uses l:____ syntax
                twt = i.group(1)
                lcol = ltweet(twt)
                if lcol:
                    twtFlag = True
                    twts += 1
                    id,time = tattrs(contents,i)
                    print "  %s" % twt
#                    try:
                    print "    id: %s; time: %s" % (id,time)
                    print >>out,"  tweet: %s" % twt
                    print >>out,"    id: %s; time: %s" % (id,time)
                    print >>file,"%s$xyzzy$%s$xyzzy$%s" % (lcol[0],id,time)
#                    except:
#                        print "  error parsing tweet!"
            if twtFlag:
                twtusers += 1

    if not options.f:
        percent = locusers/numusers         # % users with location 
        pcoord = coordusers/numusers        # % users with coordinates
        plcoord = coordusers/locusers       # % locations that have coordinates
        ptweet = twtusers/numusers          # % users using l:____
        pvaddr = vaddr/locusers             # % users with valid address
        print >>out,"\n\n##############################"
        print >>out,"number of users: %d" % numusers
        print >>out,"------------------------------"
        print >>out,"number of users with location: %d" % locusers
        print >>out,"percentage users with location: %f" % percent
        print >>out,"------------------------------"
        print >>out,"number of users with coordinates: %d" % coordusers
        print >>out,"percentage users with coordinates: %f" % pcoord
        print >>out,"percentage location users with coordinates: %f" % plcoord
        print >>out,"------------------------------"
        if options.m: #metacarta was used
            print >>out,"number of errors logging into MetaCarta: %d" % login
            print >>out,"number of users with valid address: %d" % vaddr
            print >>out,"percentage location users with valid address: %f" % pvaddr
            print >>out,"------------------------------"
        if options.t: #tweets were parsed
            print >>out,"number of tweets with l:____: %d" % twts
            print >>out,"number of users using l:____: %d" % twtusers
            print >>out,"percentage users using l:____: %f" % ptweet
            print >>out,"------------------------------"
        print >>out,"\n*location user: a user who specifies a location in their profile"
        if options.m:
            print >>out,"\n*valid address: address in user profile either:"
            print >>out,"    a) specified coordinates;"
            print >>out,"    b) matched only one location using MetaCarta."

    users.close()

parser = OptionParser()
parser.add_option(                      #directory with user pages
    "-d",
    "--directory",
    dest="d",
    metavar="DIR",
    default="/project/wdim/crawlData/good_sample/",
    help="directory to find user pages in" )
parser.add_option(                      #one file in directory
    "-f",
    "--file",
    dest="f",
    metavar="ONLY_FILE",
    default=False,
    help="single file in directory to run")
parser.add_option(                      #metacarta
    "-m",
    "--no-metacarta",
    action="store_false",
    dest="m",
    default=True,
    help="do not process location information in profile using MetaCarta")
parser.add_option(                      #output file
    "-o",
    "--outfile",
    dest="o",
    metavar="OUTPUT_FILE",
    default="cData.txt",
    help="file to write output of location data extracted by crawl")
parser.add_option(                      #use stdout for output
    "-s",
    "--stdout",
    action="store_true",
    dest="s",
    default=False,
    help="use standard output instead of output file")
parser.add_option(                      #tweets
    "-t",
    "--no-tweets",
    action="store_false",
    dest="t",
    default=True,
    help="do not process l:____ matches found in user tweets")
parser.add_option(                      #file for user listing
    "-u",
    "--ufile",
    dest="u",
    metavar="USER_FILE",
    default="users.txt",
    help="file to write user page names to")
parser.add_option(                      #verbose
    "-v",
    "--verbose",
    action="store_true",
    dest="v",
    default=False,
    help="turn on verbose mode" )

if __name__ == "__main__":
    main()
