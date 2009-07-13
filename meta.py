#!/usr/bin/env python

from sys import argv
from os import mkdir
from urllib import urlopen
import simplejson as json
from location import loc
import metacarta
import commands


def userLoc(username,ts):
    dir = "data/addresses/" #local directory
    local = False           #location found locally
    file = False            #location found in file
    web = False             #location found on web
    adr = False             #location given in user profile
    coords = False          #coordinates given in user profile
    lat = False             #latitude of user
    lon = False             #longitude of user
    path = False            #path obtained from MetaCarta
    #### ATTEMPT LOCAL RETRIEVAL ####
    try:
        lfile = open("%s%s/%s.loc"%(dir,username[0].lower(),username),'r')
        contents = lfile.read()[:-1]
        adr,lat,lon,path,ts = contents.split("$xyzzy$")
        lfile.close()
        local = True        
    except:
        local = False
    #### ATTEMPT FILE RETRIEVAL ####
#    if not local:
#        d = "/project/wdim/crawlData/20_tweet_public_timeline/Updates/"
#        try:
#            ufile = open("%s%s.html" % (d,username),'r')
#            contents = ufile.read()
#            adr,coords = loc(contents)
#            file = True
#        except:
#            file = False
#    #### GET FROM WEB ####
    if not file:
        url = "http://www.twitter.com/%s" % username
        try:
            page = urlopen(url)
            html = page.read()
            adr, coords = loc(html)
            web = True
        except:
            print "  error accessing webpage"
            efile = open("spatial.err",'a')
            print >>efile,username
            efile.close()
    #### IF NOT LOCAL, MAKE LOCAL ####
    if file or web:
        if coords: #coordinates given
            lat = coords[0]
            lon = coords[1]
        else: #location given, but not coordinates
            if adr != False:
                leng,path,cent,box,pop = findLoc(adr)
                if leng > 0:
                    lat = cent["Latitude"]
                    lon = cent["Longitude"]
        lfile = open("%s%s/%s.loc"%(dir,username[0].lower(),username),'w')
        uline = "%s$xyzzy$%s$xyzzy$%s$xyzzy$%s$xyzzy$%s\n"
        lfile.write(uline % (adr,lat,lon,path,ts))
    return [adr,lat,lon,path,ts]


def findLoc(adr):
    data,error = locationfinder(adr)
    while error:
        data,error = locationfinder(adr)
    leng = len(data["Locations"])
    try:
        loc = data["Locations"][0]
        path = loc["Paths"]["Administrative"]
        cent = loc["Centroid"]
        box = loc["ViewBox"]
        pop = loc["Population"]
    except:
        loc = False
        path = False
        cent = False
        box = False
        pop = False
    return [leng,path,cent,box,pop]


def in_city(lat,lon,city):
    flag = False
    len,path,cent,box,pop = findLoc(city)
    latOK = box["MinLatitude"] < lat < box["MaxLatitude"]
    lonOK = box["MinLongitude"] < lon < box["MaxLongitude"]
    if latOK and lonOK:
        flag = True
    return flag


def locationfinder(adr):
    error = False
    data = False
    lf = metacarta.LocationFinder("bw1224@messiah.edu","tamuresearcher")
    lf.method = "LocationFinder"
#    print "method: %s" % lf.method
    try:
        data = lf.request({'query':adr})
    except:
        error = True
    return [data,error]


def storeLocs():
    dir = "/project/wdim/crawlData/20_tweet_public_timeline/Updates/"
    statout = commands.getstatusoutput("ls %s | grep \".html\" > users.txt" % dir)
    ufile = open("users.txt",'r')
    d = {}
    line = 0
    for user in ufile:
        line += 1
        if line%100 != 0:
            continue
        user = user[:-1]
        username = user[:user.rfind('.')]
        print username
        ufile = open("%s%s"%(dir,user))
        contents = ufile.read()
        userLoc,coords = loc(contents)
        flag = True
        while flag:
            data,error = locationfinder(userLoc)
            if not error:
                flag = False
        if not error:
            try:
                locat = data["Locations"][0]
                path = locat["Paths"]["Administrative"]
                leng = len(path)
                country = path[leng-1]
                try:
                    d[country]["total"] += 1
                except:
                    d[country] = {}
                    d[country]["total"] = 1
                state = path[leng-2]
                try:
                    d[country][state] += 1
                except:
                    d[country][state] = 1
            except:
                print "country or state not found"
        else:
            print "error logging into metacarta"
    ufile.close()
    dfile = open("locdist.csv",'w')
    for country in d.keys():
        try:
            dfile.write("\n%s,%d\n"%(country,d[country]["total"]))
        except:
            print "error decoding country"
        for state in d[country].keys():
            if state != "total":
                try:
                    dfile.write("%s,%d\n"%(state,d[country][state]))
                except:
                    print "error decoding state"
    dfile.close()


def main():
    username = argv[1]
    print userLoc(username)


if __name__ == "__main__":
    main()
