#!/usr/bin/env python

from optparse import OptionParser
import commands

def startT(file,cLat,cLon):
    print >>file,"<html>"
    print >>file,"  <head>"
    print >>file,"    <link href=\"default.css\" rel=\"stylesheet\" type=\"text/css\" />"
    print >>file,"    <title>Bethany Waldmann | CSE@TAMU REU</title>\n"
    print >>file,"    <meta name=\"viewport\" content=\"initial-scale=1.0, user-scalable=no\" />"
    print >>file,"    <script type=\"text/javascript\" src=\"http://maps.google.com/maps/api/js?sensor=false\"></script>"
    print >>file,"    <script type=\"text/javascript\">"
    print >>file,"      function initialize() {"
    print >>file,"          var coord0 = new google.maps.LatLng(%s,%s);" % (cLat,cLon)
    print >>file,"          var myOptions = {"
    print >>file,"              zoom: 2,"
    print >>file,"              center: coord0,"
    print >>file,"              mapTypeId: google.maps.MapTypeId.TERRAIN,"
    print >>file,"          };"
    print >>file,"          var map = new google.maps.Map(document.getElementById(\"map_canvas\"), myOptions);\n"

def userT(file,num,username,lat,lon):
    print >>file,"          var coord%d = new google.maps.LatLng(%s,%s);" % (num,lat,lon)
    print >>file,"          var marker%d = new google.maps.Marker({" % num
    print >>file,"              position: coord%d," % num
    print >>file,"              map: map,"
    print >>file,"              title:\"%s\"});\n" % username

def endT(file):
    print >>file,"      }"
    print >>file,"    </script>\n"
    print >>file,"  </head>\n"
    print >>file,"  <body onload=\"initialize()\">"
    print >>file,"    <div id=\"container\">\n"
    print >>file,"    <div id=\"Header\">"
    print >>file,"        <h3><a href=\"index.php\">Bethany Waldmann</a> | CSE@TAMU REU 2009</h3>"
    print >>file,"    </div>\n"
    print >>file,"    <div id=\"Menu\">"
    print >>file,"        <a href=\"index.php\">Home</a><br>"
    print >>file,"        <a href=\"aboutme.php\">About Me</a><br>"
    print >>file,"        <a href=\"mymentors.php\">My Mentors</a><br>"
    print >>file,"        <a href=\"research.php\">Research</a><br>"
    print >>file,"        <a href=\"journal.php\">Journal</a><br>"
    print >>file,"        <a href=\"resources.php\">Resources</a><br>"
    print >>file,"        <a href=\"maps.php\">Maps</a><br>"
    print >>file,"    </div>\n"
    print >>file,"    <div id=\"Content\">"

def writeM(file,title):
    print >>file,"<?php include(\"topM.html\"); ?>\n"
    print >>file,"        <div id=\"entry\">"
    print >>file,"            <h4>%s</h4>" % title
    print >>file,"            <div id=\"map_canvas\" style=\"width:100%; height:75%\"></div>"
    print >>file,"        </div>\n"
    print >>file,"<?php include(\"bottom.html\"); ?>"

def main():
    (options,args) = parser.parse_args()
    mfile = open(options.m,'w')         #map file
    writeM(mfile,"Twitter Users")
    tfile = open(options.t,'w')         #top file
    startT(tfile,38,-27)
    if options.f:
        ufile = open(options.u,'w')
        print >>ufile,options.f
        ufile.close()
    else:
        statout = commands.getstatusoutput("ls %s > %s" % (options.d,options.u))
    users = open(options.u,'r')         #user listing
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
            print "  lat: %s; lon: %s" % (lat,lon)
            if lat and lon and num<37:
                userT(tfile,num,username,lat,lon)
                num += 1
        except:
            print "  error unpacking location"

    endT(tfile)

parser = OptionParser()
parser.add_option(                      #directory with user data
    "-d",
    "--directory",
    dest="d",
    metavar="DIR",
    default="tmp/",
    help="directory to find user data in" )
parser.add_option(                      #one file in directory
    "-f",
    "--file",
    dest="f",
    metavar="ONLY_FILE",
    default=False,
    help="single file in directory to run")
parser.add_option(                      #map file
    "-m",
    "--mapfile",
    dest="m",
    metavar="MAP_FILE",
    default="maps.php",
    help="file to write map content to")
parser.add_option(                      #use stdout for output
    "-s",
    "--stdout",
    action="store_true",
    dest="s",
    default=False,
    help="use standard output instead of output file")
parser.add_option(                      #top file
    "-t",
    "--topfile",
    dest="t",
    metavar="TOP_FILE",
    default="topM.html",
    help="file to write opening html tags and javascript to")
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
