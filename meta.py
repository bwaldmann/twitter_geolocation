
#!/usr/bin/env python

from sys import argv
from urllib import urlopen
import simplejson as json
from location import loc
import metacarta



def userLoc(username):
    dir = "data/addresses/"
    file = False #username stored in file
    try:
        lfile = open("%s%s.txt"%(dir,username[0]),'r')
        contents = lfile.read()[:-2]
        lfile.close()
        d = json.loads("{%s}"%contents)
        adr,lat,lon,meta = d[username]
        adr = adr.encode("ascii","replace") #convert from unicode
        file = True        
    except:
        print "user location not stored locally"
    if not file:
        url = "http://www.twitter.com/%s" % username
        page = urlopen(url)
        html = page.read()
        meta = "false"
        adr, coords = loc(html)
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


def main():
    username = argv[1]
    print userLoc(username)


if __name__ == "__main__":
    main()
