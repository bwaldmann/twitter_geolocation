#!/usr/bin/env python

import commands
from meta import locationfinder
from os import mkdir


def main():
    dir = "/project/wdim/geosocial"
    statout = commands.getstatusoutput("ls %s/paths/residents > bin/paths.list" % dir)
    paths = open("bin/paths.list",'r')
    for path in paths:
        path = path[:path.rfind('.')]
        mpath = ", ".join(path.split('.'))
        print mpath
        error = True
        while error:
            data,error = locationfinder(mpath)
        try:
            loc = data["Locations"][0]
            cent = loc["Centroid"]
            box = loc["ViewBox"]
            pop = loc["Population"]
            type = data["Types"][loc["Type"]]["ShortDescription"]
            try:
                file = open("%s/paths/info/%s/%s.info"%(dir,type,path),'w')
            except:
                mkdir("%s/paths/info/%s"%(dir,type))
                file = open("%s/paths/info/%s/%s.info"%(dir,type,path),'w')
            print >>file,"%s$xyzzy$%s$xyzzy$%s$xyzzy$%s" % (pop,cent,type,box)
            file.close()
        except:
            efile = open("info.errfile",'a')
            print >>efile,path
            efile.close()


if __name__ == "__main__":
    main()
