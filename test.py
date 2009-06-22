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

def childProc(num):
    print "*in %d*" % num
    sleep(10)
    print "*done %d*" % num

def main():
    log = open("test.log",'w')
    tmp = range(20)
    print tmp
    proc = []                           #child processes (current)
    for num in tmp: #for each number 0-19
        cpid = fork()
        if not cpid:
            childProc(num)
            sys.exit()
        if cpid: #parent process
            print "starting child process: %d" % cpid
            proc.append(cpid)
            while len(proc)>=10: #10 child processes running
                print "checking child processes"
                print "  %s" % proc
                for c in proc:
                    print "  checking %d... %s" % (c,is_running(c))
                    if not is_running(c):
                        print "  child process done: %d" % c
                        proc.remove(c)
                print "%d processes running - waiting..." % len(proc)
                sleep(3) #wait 3 seconds
            continue




if __name__ == "__main__":
    main()
