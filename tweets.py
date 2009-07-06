#!/usr/bin/env python

import sys
import commands
import re
from os import mkdir
from optparse import OptionParser
from datetime import date,datetime
from codes import codeReg, find_airport_code


def findTweets(contents):
    tweets = []
    m = 0
    while True:
        try:
            print "CCC %s" % contents[m:]
            start1 = contents[m:].find("status_")
            if start1 == -1:
                print "error finding id"
                break
            start1 += m + 7 # len("status_") = 7
            end1 = start1+contents[start1:].find('\"')
            print "startID: %s; endID: %s" % (start1,end1)
            id = contents[start1:end1]
            print "id: %s" % id
            start2 = contents[end1:].find("<span class=\"entry-content\">")
            if start2 == -1:
                print "error finding tweet"
                break
            start2 += m + end1 + 28
            end2 = start2+contents[start2:].find("</span><span entry=\"meta entry-meta\">")
            print "startTwt: %s; endTwt: %s" % (start2,end2)
            twt = contents[start2:end2]
            print "tweet: %s" % twt
            t = re.compile("<span class=\"published\" title=\"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})",re.I)
            c = contents[end2:]
            print "what we have to work with for timestamp: %s" % c
            time = t.search(c).group(1)
            print "TWEET PARSED! id: %s; twt: %s; time: %s" % (id,twt,time)
            tweets.append([id,twt,time])
            m = end2
            print "m: %d" % m
        except:
            break
    return tweets

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
    prtusers = 0.0                      #number of airport-code users
    prtuses = 0.0                       #number of airport-code uses
    reg = codeReg()
    for line in users: #for each user in listing
        numusers += 1
        user = options.d+line[0:-1] #absolute path to user page
        username = user[user.rfind('/')+1:user.rfind('.')] #isolate username
        tfile = open("%s%s.twt" % (dir,username),'w')
#        cfile = open("%s%s.apt" % (dir,username),'w')
        print username #TEMPORARY
        if options.v: #verbose option
            print >>out,username
        page = open(user,'r')
        contents = page.read()          #user page contents (html)
        page.close()
        cflag = False                   #user used airport code
        tweets = findTweets(contents)   #all user's tweets
        for t in tweets:
            id,twt,time = t
            print >>tfile,"%s$xyzzy$%s$xyzzy$%s" % (twt,id,time)
            code = find_airport_code(twt,reg)
            for c in code:
                cflag = True
                prtuses += 1
#                print >>cfile,"%s; %s" % (username,twt)
                if c in codes: #airport already identified
                    codes[c] += 1
                else: #airport not yet identified
                    codes[c] = 1
            if cflag:
                prtusers += 1
    print codes
    print "codes used: %d" % prtuses
    print "unique codes used: %d" % len(codes)
    print "airport-code users: %d" % prtusers
                

#    if not options.f:
#        percent = locusers/numusers         # % users with location 
#        pcoord = coordusers/numusers        # % users with coordinates
#        plcoord = coordusers/locusers       # % locations that have coordinates
#        ptweet = twtusers/numusers          # % users using l:____
#        pvaddr = vaddr/locusers             # % users with valid address
#        print >>out,"\n\n##############################"
#        print >>out,"number of users: %d" % numusers
#        print >>out,"------------------------------"
#        print >>out,"number of users with location: %d" % locusers
#        print >>out,"percentage users with location: %f" % percent
#        print >>out,"------------------------------"
#        print >>out,"number of users with coordinates: %d" % coordusers
#        print >>out,"percentage users with coordinates: %f" % pcoord
#        print >>out,"percentage location users with coordinates: %f" % plcoord
#        print >>out,"------------------------------"
#        if options.m: #metacarta was used
#            print >>out,"number of errors logging into MetaCarta: %d" % login
#            print >>out,"number of users with valid address: %d" % vaddr
#            print >>out,"percentage location users with valid address: %f" % pvaddr
#            print >>out,"------------------------------"
#        if options.t: #tweets were parsed
#            print >>out,"number of tweets with l:____: %d" % twts
#            print >>out,"number of users using l:____: %d" % twtusers
#            print >>out,"percentage users using l:____: %f" % ptweet
#            print >>out,"------------------------------"
#        print >>out,"\n*location user: a user who specifies a location in their profile"
#        if options.m:
#            print >>out,"\n*valid address: address in user profile either:"
#            print >>out,"    a) specified coordinates;"
#            print >>out,"    b) matched only one location using MetaCarta."

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
