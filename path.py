#!/usr/bin/env python

import commands
from os import fork


def main():
    dir1 = "data/addresses"
    dir2 = "data/paths"
    for i in range(10):
        cid = fork()
        if cid:
            continue
        cfile = open("bin/char%d.txt"%i,'r')
        for char in cfile:
            char = char[:-1]
            print char
            statout = commands.getstatusoutput("ls %s/%s > bin/%s_local.list" % (dir1,char,char))
            ufile = open("bin/%s_local.list"%char)
            for user in ufile:
                user = user[:-1]
                username = user[:user.rfind('.')]
                print username
                lfile = open("%s/%s/%s" % (dir1,username[0].lower(),user),'r')
                contents = lfile.read()
                adr,lat,lon,path,ts = contents.split("$xyzzy$")
                if path != "False":
                    try:
                        path = path.split(',')
                    except:
                        print "len(path) = 1"
                    st = ""
                    for region in path:
                        region = region[region.find('\'')+1:region.rfind('\'')]
#                        print region
                        st += "%s." % region
#                    print st[:-1]
                    ofile = open("%s/%s.residents"%(dir2,st[:-1]),'a')
                    print >>ofile,username
                    ofile.close()
                else:
                    if adr != False:
                        ofile = open("%s/nometa.list" % dir2,'a')
                        print >>ofile,"%s$xyzzy$%s" % (username,adr)
                        ofile.close()
                    else:
                        ofile = open("%s/noadr.list" % dir2,'a')
                        print >>ofile,username
                        ofile.close()


if __name__ == "__main__":
    main()
