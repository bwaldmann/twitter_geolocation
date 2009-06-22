#!/usr/bin/env python

import sys
from time import sleep
from os import pipe, fdopen, fork, close, getpid, getppid, kill
import signal


#inspired by http://mail.python.org/pipermail/python-list/2002-May/144522.html
def is_running(pid):
    try:
        kill(pid,0)
        return 1
    except:
        return 0

def main():
    log = open("test.log",'w')
    tmp = range(20)
    print tmp
    proc = []                           #child processes (current)
    for item in tmp: #for each user in listing
        cpid = fork()
        if cpid: #parent process
            print >>log,"starting child process: %d" % cpid
            proc.append(cpid)
            while len(proc)>=10: #10 child processes running
                print >>log,"checking child processes"
                print >>log,"  %s" % proc
                for c in proc:
                    print >>log,"  checking %d... %s" % (c,is_running(c))
                    if not is_running(c):
                        print >>log,"  child process done: %d" % c
                        proc.remove(c)
                print >>log,"%d processes running - waiting..." % len(proc)
                sleep(3) #wait 3 seconds
            continue
        #child process
        print >>log,"*in %d*" % item
        sleep(10)
        print >>log,"*done %d*" % item
        kill(getpid(),signal.SIG_DFL)

if __name__ == "__main__":
    main()
