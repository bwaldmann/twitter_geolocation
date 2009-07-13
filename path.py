#!/usr/bin/env python

import commands


def main():
    dir = "data/addresses/"
    cfile = open("bin/chars.txt",'r')
    for char in cfile:
        char = char[:-1]
        statout = commands.getstatusoutput("ls %s > bin/%s_local.list" % (dir+char,char))
        ufile = open("bin/%s_local.list"%char)
        for user in ufile:
            user = user[:-1]
            username = user[:user.rfind('.')]
            lfile = open("%s%s/%s" % (dir,username[0].lower(),user),'r')
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
                    print region
                    st += "%s." % region
                print st
                ofile = open("data/addresses/%spath"%st,'a')
                print >>ofile,username
                ofile.close()
                


if __name__ == "__main__":
    main()
