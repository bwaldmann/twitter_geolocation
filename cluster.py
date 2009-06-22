#!/usr/bin/env python

# taken from http://www.daniweb.com/forums/thread31449.html

# clustering.py contains classes and functions that cluster data points
import sys, math, random
from sphereDist import dist_on_earth


# -- The Point class represents points in n-dimensional space
class Point:
    # Instance variables
    # self.coords is a list of coordinates for this Point
    # self.n is the number of dimensions this Point lives in (ie, its space)
    # self.reference is an object bound to this Point
    # Initialize new Points
    def __init__(self, coords, reference=None):
        self.coords = coords
        self.n = len(coords)
        self.reference = reference
    # Return a string representation of this Point
    def __repr__(self):
        return str(self.coords)


# -- The Cluster class represents clusters of points in n-dimensional space
class Cluster:
    # Instance variables
    # self.points is a list of Points associated with this Cluster
    # self.n is the number of dimensions this Cluster's Points live in
    # self.centroid is the sample mean Point of this Cluster

    def __init__(self, points):
        # We forbid empty Clusters (they don't make mathematical sense!)
        if len(points) == 0: raise Exception("ILLEGAL: EMPTY CLUSTER")
        self.points = points
        self.n = points[0].n
        # We also forbid Clusters containing Points in different spaces
        # Ie, no Clusters with 2D Points and 3D Points
        for p in points:
            if p.n != self.n: raise Exception("ILLEGAL: MULTISPACE CLUSTER")
        # Figure out what the centroid of this Cluster should be
        self.centroid = self.calculateCentroid()

    # Return a string representation of this Cluster
    def __repr__(self):
        return str(self.points)

    # Update function for the <strong class="highlight">K-means</strong> algorithm
    # Assigns a new list of Points to this Cluster, returns centroid difference
    def update(self, points):
        old_centroid = self.centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        return dist_on_earth(old_centroid.coords, self.centroid.coords)

    # Calculates the centroid Point - the centroid is the sample mean Point
    # (in plain English, the average of all the Points in the Cluster)
    def calculateCentroid(self):
        centroid_coords = []
        # For each coordinate:
        for i in range(self.n):
            # Take the average across all Points
            centroid_coords.append(0.0)
            for p in self.points:
                centroid_coords[i] = centroid_coords[i]+p.coords[i]
            try:
                centroid_coords[i] = centroid_coords[i]/len(self.points)
            except:
                continue
        # Return a Point object using the average coordinates
        return Point(centroid_coords)


# -- Return Clusters of Points formed by <strong class="highlight">K-means</strong> clustering
def kmeans(points, k, cutoff):
    tmp = []
    for p in points:
        print p
        try:
            lat = float(p[1])
            lon = float(p[2])
            tmp.append(Point([lat,lon]))
        except:
            continue
    points = tmp
    # Randomly sample k Points from the points list, build Clusters around them
    initial = random.sample(points, k)
    clusters = []
    for p in initial: clusters.append(Cluster([p]))
    print "  clusters: %s" % clusters
    # Enter the program loop
    while True:
        # Make a list for each Cluster
        lists = []
        for c in clusters: lists.append([])
        # For each Point:
        for p in points:
            # Figure out which Cluster's centroid is the nearest
            smallest_distance = dist_on_earth(p.coords, clusters[0].centroid.coords)
            index = 0
            for i in range(len(clusters[1:])):
                distance = dist_on_earth(p.coords, clusters[i+1].centroid.coords)
                if distance < smallest_distance:
                    smallest_distance = distance
                    index = i+1
            # Add this Point to that Cluster's corresponding list
            lists[index].append(p)
        # Update each Cluster with the corresponding list
        # Record the biggest centroid shift for any Cluster
        biggest_shift = 0.0
        for i in range(len(clusters)):
            shift = clusters[i].update(lists[i])
            biggest_shift = max(biggest_shift, shift)
        # If the biggest centroid shift is less than the cutoff, stop
        if biggest_shift < cutoff: break
    tmp = []
    for c in clusters:
        tmp.append([len(c.points),c.centroid.coords])
    return tmp
    # Return the list of cluster attributes
    return tmp


# -- Get the Euclidean distance between two Points
def getDistance(a, b):
    # Forbid measurements between Points in different spaces
    if a.n != b.n: raise Exception("ILLEGAL: NON-COMPARABLE POINTS")
    # Euclidean distance between a and b is sqrt(sum((a[i]-b[i])^2) for all i)
    ret = 0.0
    for i in range(a.n):
        ret = ret+pow((a.coords[i]-b.coords[i]), 2)
    return math.sqrt(ret)


# -- Create a random Point in n-dimensional space
def makeRandomPoint(n, lower, upper):
    coords = []
    for i in range(n): coords.append(random.uniform(lower, upper))
    return Point(coords)


# -- Main function
def main(args):
    num_points, n, k, cutoff, lower, upper = 10, 2, 3, 0.5, -200, 200
    # Create num_points random Points in n-dimensional space
    points = []
    for i in range(num_points): points.append(makeRandomPoint(n, lower, upper))
    # Cluster the points using the <strong class="highlight">K-means</strong> algorithm
    clusters = kmeans(points, k, cutoff)
    # Print the results
    print "\nPOINTS:"
    for p in points: print "P:", p
    print "\nCLUSTERS:"
    for c in clusters: print "C:", c


# -- The following <strong class="highlight">code</strong> executes upon command-line invocation
if __name__ == "__main__": main(sys.argv)
