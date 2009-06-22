#!/usr/bin/env python
 
import sys
from time import sleep
from os import pipe, fdopen, fork, close, getpid, getppid, kill
import signal

MAX_PROCS = 5

 
#inspired by http://mail.python.org/pipermail/python-list/2002-May/144522.html
def is_running(pid):
    try: return kill(pid,0)
    except: return False


def childProc(num):
    cfile = open("tmp/fork%d.txt" % num,'w')
    print >>cfile,"*in %d*" % num
    sleep(10)
    print >>cfile,"*done %d*" % num
    cfile.close()
    sys.exit()


def watch_the_children(proc): 
    while len(proc)>=MAX_PROCS: #10 child processes running
        for c in proc:
            if not is_running(c):
                print "  child process done: %d" % c
                proc.remove(c)
        print "SLEEPING %d processes running - waiting..." % len(proc)
        sleep(3) #wait 3 seconds


def main():
    log = open("test.log",'w')
    proc = []                           #child processes (current)
    for num in range(10): #for each number 0-19
        cpid = fork()
        if cpid: #parent process
            print "NEWCHILD:%d PARENT:%d numOfKid:%d" % (cpid,getpid(),num)
            proc.append(cpid)
            watch_the_children(proc)
        else:
            childProc(num)


if __name__ == "__main__":
    main()
