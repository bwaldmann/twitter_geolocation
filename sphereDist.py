#!/usr/bin/env python

import sys
from math import pi, sin, cos, acos


def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # taken from http://www.johndcook.com/python_longitude_latitude.html
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = pi/180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude

    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    cosv = (sin(phi1)*sin(phi2)*cos(theta1 - theta2) +
           cos(phi1)*cos(phi2))
    arc = acos( cosv )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    # returns distance in feet
    return arc * 3960 * 5280

def main():
    lat1 = float(sys.argv[1])
    lon1 = float(sys.argv[2])
    lat2 = float(sys.argv[3])
    lon2 = float(sys.argv[4])
    print "[%f,%f], [%f,%f]" % (lat1,lon1,lat2,lon2)
    print "  distance: %f miles" % dist_on_earth([lat1,lon1],[lat2,lon2])

if __name__ == "__main__":
    main()
