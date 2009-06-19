#!/usr/bin/env python

from optparse import OptionParser
import commands
from cluster import kmeans

def startT(cLat,cLon):
    cLat,cLon

def userT(num,username,lat,lon):
    num,lat,lon,num,num,username

def writeM(file,title):
    title

def main():
    (options,args) = parser.parse_args()
    mfile = open(options.m,'w')         #map file
    print >>mfile,open(options.input1).read() % ("Twitter Users")
    print >>mfile,open(options.input2).read()
    sfile = open(options.script,'w')    #script file
    initialize = open(options.initialize,'r').read()
    print >>sfile,initialize % (38,-27)
    if options.f:
        ufile = open(options.u,'w')
        print >>ufile,options.f
        ufile.close()
    else:
        statout = commands.getstatusoutput("ls %s > %s" % (options.d,options.u))
    users = open(options.u,'r')         #user listing
    points = []
    num = 1
    for line in users: #for each user in listing
        user = options.d+line[0:-1] #absolute path to user data
        print "user: "+user
        username = user[user.rfind('/')+1:user.rfind('.')] #isolate username
        print username
        if options.v: #verbose option
            print username
        data = open(user,'r')           #user data file
        line1 = data.readline()
        try:
            add,lat,lon = line1.split('$xyzzy$')
            lon = lon[:-1]
            if lat and lon:
                points.append([username,lat,lon])
#            print "  lat: %s; lon: %s" % (lat,lon)
#            if lat and lon and num<37:
#                marker = open(options.marker).read()
#                print >>sfile, marker % (num,lat,lon,num,num,username)
#                num += 1
        except:
            print "  error unpacking location"
#    print "points: %s" % points
    markers = kmeans(points,50,200)     #clusters of users
    print "markers: %s" % markers
    i = 0                               #counter
    for m in markers:
        num = m[0]                      #number of members in cluster
        lat = m[1][0]                   #latitude of cluster mean
        lon = m[1][1]                   #longitude of cluster mean
        marker = open(options.marker).read()
        print >>sfile,marker % (i,lat,lon,i,i,num)
        i += 1
    print >>sfile,open(options.close,'r').read()

parser = OptionParser()
parser.add_option(                      #script closure file
    "--close",
    dest="close",
    metavar="FILE",
    default="close.html",
    help="file to read script closure from")
parser.add_option(                      #directory with user data
    "-d",
    "--directory",
    dest="d",
    metavar="DIR",
    default="tmp/",
    help="directory to find user data in")
parser.add_option(                      #one file in directory
    "-f",
    "--file",
    dest="f",
    metavar="FILE",
    default=False,
    help="single file in directory to run")
parser.add_option(                      #script initialization file
    "--initialize",
    dest="initialize",
    metavar="FILE",
    default="initialize.html",
    help="file to read script initialization from")
parser.add_option(                      #beginning of maps.php input file
    "--input1",
    dest="input1",
    metavar="FILE",
    default="input1.html",
    help="file to read beginning of maps.php from")
parser.add_option(                      #end of maps.php input file
    "--input2",
    dest="input2",
    metavar="FILE",
    default="input2.html",
    help="file to read end of maps.php from")
parser.add_option(                      #map file
    "-m",
    "--mapfile",
    dest="m",
    metavar="FILE",
    default="maps.php",
    help="file to write map content to")
parser.add_option(                      #marker input file
    "--marker",
    dest="marker",
    metavar="FILE",
    default="marker.html",
    help="file to read marker section of script from")
parser.add_option(                      #use stdout for output
    "-s",
    "--stdout",
    action="store_true",
    dest="s",
    default=False,
    help="use standard output instead of output file")
parser.add_option(                      #top file
    "--script",
    dest="script",
    metavar="FILE",
    default="script.html",
    help="file to write javascript to")
parser.add_option(                      #file for user listing
   "-u",
    "--ufile",
    dest="u",
    metavar="USER_FILE",
    default="users.txt",
    help="file to write user data names to")
parser.add_option(                      #verbose
    "-v",
    "--verbose",
    action="store_true",
    dest="v",
    default=False,
    help="turn on verbose mode" )

if __name__ == "__main__":
    main()
