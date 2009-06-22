#!/usr/bin/env python
 
import sys
from time import sleep
from os import pipe, fdopen, fork, close, getpid, getppid, kill
import signal
 
 
#inspired by http://mail.python.org/pipermail/python-list/2002-May/144522.html
def is_running(pid):
    try:
        return kill(pid,0)
    except:
        return False


def childProc(num):
    cfile = open("tmp/fork%d.txt" % num,'w')
    print >>cfile,"*in %d*" % num
    sleep(10)
    print >>cfile,"*done %d*" % num
    cfile.close()

 
def main():
    log = open("test.log",'w')
    tmp = range(20)
    print tmp
    proc = []                           #child processes (current)
    for num in tmp: #for each number 0-19
        cpid = fork()
        if cpid: #parent process
            print "process %d starting child process: %d" % (getpid(),cpid)
            proc.append(cpid)
            while len(proc)>=10: #10 child processes running
                print "checking child processes"
                print "  %s" % proc
                for c in proc:
                    if not is_running(c):
                        print "  child process done: %d" % c
                        proc.remove(c)
                    else:
                        print "  running %d" % c
                print "%d processes running - waiting..." % len(proc)
                sleep(3) #wait 3 seconds
        else:
            childProc(num)
            sys.exit()
    sys.exit()
 
 
if __name__ == "__main__":
    main()
