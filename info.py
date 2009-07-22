#!/usr/bin/env python

import commands
from meta import locationfinder
from os import mkdir


def storeInfo(dir,path,mpath):
    error = True
    while error:
        data,error = locationfinder(mpath)
    try:
        loc = data["Locations"][0]
        cent = loc["Centroid"]
        box = loc["ViewBox"]
        pop = loc["Population"]
        type = data["Types"][loc["Type"]]["ShortDescription"]
        file = open("%s/paths/info/%s.info"%(dir,path),'w')
        print >>file,"%s$xyzzy$%s$xyzzy$%s$xyzzy$%s" % (pop,cent,type,box)
        file.close()
        return [pop,cent,type,box]
    except:
        efile = open("storeInfo.err",'a')
        print >>efile,path
        efile.close()


def main():
    dir = "/project/wdim/geosocial"
    statout = commands.getstatusoutput("ls %s/paths/residents > bin/paths.list" % dir)
    paths = open("bin/paths.list",'r')
    for path in paths:
        path = path[:path.rfind('.')]
        mpath = ", ".join(path.split('.'))
        print mpath
        storeInfo(dir,path,mpath)


if __name__ == "__main__":
    main()
