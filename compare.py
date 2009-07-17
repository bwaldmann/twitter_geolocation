#!/usr/bin/env python

import commands
from sys import argv, stdin, stdout, exit
from meta import locationfinder
from sphericalDist import dist_on_earth


def getCities(dir,num,txt):
    stat,out = commands.getstatusoutput("ls %s | grep %s.*" % (dir,txt))
    count = 1
    selections = []
    for line in out:
        selections.append[count,line[:-1]]
        count += 1
    print "count: %d" % count
    print "city %d options:" % num
    for option in selections:
        print "  %d: %s" % (option[0],option[1])
    print "  %d: EXIT" % count
    print "select city %d: " % num,
    cref = int(stdin.readline())
    if cref == count:
        exit()
    city = selections[cref][1]
    return city


def getCityInfo(txt):
    path = ", ".join(txt.split('.'))
    print path
    #### TRY TO GET INFO LOCALLY ####
    try:
        info = open("%s.info"%path,'r')
        info = info.read()
        pop,cent,type,box = info.split("$xyzzy$")
    #### GET INFO FROM METACARTA (STORE LOCALLY) ####
    except:
        error = True
        while error:
            data,error = locationfinder(path)
        loc = data["Locations"][0]
        cent = loc["Centroid"]
        box = loc["ViewBox"]
        pop = loc["Population"]
        type = data["Types"][loc["Type"]]["ShortDescription"]
        file = open("%s.info",'w')
        print >>file,"%s$xyzzy$%s$xyzzy$%s$xyzzy$s" % (pop,cent,type,box)
        file.close()
    return pop,cent,type,box


def parseCityInfo(dir,num,txt):
    city = getCities(dir,num,txt)
    print city
    pop,cent,type,box = getCityInfo(city)
    lat = cent["Latitude"]
    lon = cent["Longitude"]    
    return city,pop,lat,lon


def getResidents(dir,city):
    residents = []
    file = open("%s/%s.path"%(dir,city))
    file = file.read()
    for line in file:
        residents.append(line[:-1])
    return residents


def getContacts(dir,residents):
    contacts = []
    for resident in residents:
        rfile = open("%s/%s.fromto"%(dir,resident),'r')
        for contact in rfile:
            contact = contact.split(' ')[1]
            contacts.append(contact)
        rfile.close()
    contacts = set(contacts)
    return contacts

def write_to_csv(cityA,cityB,popA,popB,sampA,sampB,contactsA,contactsB,AtoB,BtoA,dist)
    csvFile = open("%s-TO-%s.csv",'w')
    print >>csvFile,",%s,%s,Contacts,A to B,B to A" % (cityA,cityB)
    print >>csvFile,"Population,%d,%d,,," % (popA,popB)
    print >>csvFile,"Sample,%d,%d,%d,%d,%d" % (sampa,sampB,AtoB,BtoA)
    print >>csvFile,"Contacts,%d,%d,,," % (contactsA,contactsB)
    print >>csvfile,",,,,,"
    print >>csvfile,"Distance,%d" % dist
    csvFile.close()


def main():
    dir1 = "data/addresses"
    dir2 = "/local/dc/data/fromto"
    cityA,popA,latA,lonA = parseCityInfo(dir1,1,argv[1])
    cityB,popB,latB,lonB = parseCityInfo(dir1,2,argv[2])
    residentsA = getResidents(dir2,cityA)
    residentsB = getResidents(dir2,cityB)
    sampA = len(residentsA)
    sampB = len(residentsB)
    contactsA = getContacts(dir2,residentsA)
    contactsB = getContacts(dir2,residentsB)
    fromAtoB = len(contactsA & set(residentsB))
    fromBtoA = len(contactsB & set(residentsA))
    dist = dist_on_earth([latA,lonA],[latB,lonB])
    write_to_csv(popA,popB,sampA,sampB,len(contactsA),len(contactsB),fromAtoB,fromBtoA,dist)


if __name__ == "__main__":
    main()
