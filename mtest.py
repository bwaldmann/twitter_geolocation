#!/usr/bin/env python

import commands
from meta import userLoc
from os import fork
from datetime import date


def main():
    dir = "/local/dc/data/fromto/"
    ts = date.today()
    for i in range(10):
        cid = fork()
        if cid:
            continue
        cfile = open("bin/char%d.txt"%i,'r')
        for char in cfile:
            char = char[:-1]
            statout = commands.getstatusoutput("ls %s > bin/%s.list" % (dir+char,char))
            ufile = open("bin/%s.list"%char)
            for user in ufile:
                user = user[:-1]
                username = user[:user.rfind('.')]
                print username
                userLoc(username,ts)
            ufile.close()
        break


if __name__ == "__main__":
    main()
