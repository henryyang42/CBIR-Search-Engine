# import the necessary packages
import numpy as np
from scipy import spatial
import csv


def euclidean_dist(a, b):
    return spatial.distance.euclidean(a, b)


def hamming_dist(a, b):
    return spatial.distance.hamming(a, b)


def cosine_dist(a, b):
    return spatial.distance.cosine(a, b)


class Searcher:

    def __init__(self, indexPath):
        # store our index path
        self.indexPath = indexPath

    def search(self, queryFeatures, limit=10, distance='euclidean'):
        # initialize our dictionary of results
        results = {}
        dist_model = {
            'hamming': hamming_dist,
            'euclidean': euclidean_dist,
            'cosine': cosine_dist
        }
        dist = dist_model[distance]
        # open the index file for reading
        with open(self.indexPath) as f:
            # initialize the CSV reader
            reader = csv.reader(f)

            # loop over the rows in the index
            for row in reader:
                # parse out the image ID and features, then compute the
                # chi-squared distance between the features in our index
                # and our query features
                features = [float(x) for x in row[1:]]
                d = dist(features, queryFeatures)

                results[row[0]] = d

            # close the reader
            f.close()

        # sort our results, so that the smaller distances (i.e. the
        # more relevant images are at the front of the list)
        results = sorted([(v, k) for (k, v) in results.items()])

        # return our (limited) results
        return results[:limit]
