#!/usr/bin/env python

from sys import argv
from meta import userLoc


if __name__ == "__main__":
    username = argv[1]
    adr,lat,lon,meta = userLoc(username)
    print "adr: %s; lat: %s; lon: %s; meta: %s" % (adr,lat,lon,meta)
