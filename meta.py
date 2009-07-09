#!/usr/bin/env python

from sys import argv
from urllib import urlopen
import simplejson as json
from location import loc
import metacarta
import commands


def userLoc(username):
    dir = "data/addresses/"
    local = False #user profile stored in file
    file = False #user profile stored locally
    web = False #user profile found on web
    try:
        username = username.lower()
        lfile = open("%s%s.txt"%(dir,username[0]),'r')
        contents = lfile.read()[:-2]
        lfile.close()
        d = json.loads("{%s}"%contents)
        adr,lat,lon,meta = d[username]
        adr = adr.encode("ascii","replace") #convert from unicode
        local = True        
    except:
        print "user location not stored locally"
    if not local:
        dir = "/project/wdim/crawlData/20_tweet_public_timeline/Updates/"
        try:
            ufile = open("%s%s.html" % (dir,username),'r')
            contents = ufile.read()
            adr,coords = loc(contents)
        except:
            print "user location not stored in project/wdim/crawlData/"
    if not file:
        web = True
        url = "http://www.twitter.com/%s" % username
        page = urlopen(url)
        html = page.read()
        meta = "false"
        adr, coords = loc(html)
    if file or web:
        if adr == False: #no location given
            lat = "false"
            lon = "false"
        elif coords: #coordinates given
            lat = coords[0]
            lon = coords[1]
        else: #location given, but not coordinates
            meta = "true"
            leng,path,cent,box,pop = findLoc(adr)
            if leng > 0:
                lat = cent["Latitude"]
                lon = cent["Longitude"]
            else:
                lat = "false"
                lon = "false"
        lfile = open("%s%s.txt"%(dir,username[0]),'a')
        uline = "\"%s\":[\"%s\",%s,%s,%s],\n"
        lfile.write(uline % (username,adr,lat,lon,meta))
    return [adr,lat,lon,meta]


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
