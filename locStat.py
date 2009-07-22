#!/usr/bin/env python

from commands import getstatusoutput


def main():
    dir = "/project/wdim/geosocial/paths"
    countries = {}
    for place in open("bin/places.list"):
        try:
            place = place[:-1]
            print place
            cplace = '\ '.join(place.split())
            stat,out = getstatusoutput("wc -l %s/residents/%s"%(dir,cplace))
            path = place.split('.')[:-1]
            num = int(out.split()[0])
            try:
                countries[path[len(path)-1]] += num
            except:
                countries[path[len(path)-1]] = num
        except:
            pass
        ofile = open("out/countryPop.csv",'w')
        print >>ofile,"Country,Population,Twitter Population"
        for country in countries.keys():
            twitterPop = countries[country]
            try:
                pop = open("%s/info/%s.info"%(dir,country)).read().split("$xyzzy$")[0]
            except:
                pop = "-1"
            print >>ofile,"%s,%s,%d" % (country,pop,twitterPop)
        ofile.close()


if __name__ == "__main__":
    main()
