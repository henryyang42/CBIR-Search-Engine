from matplotlib import pyplot as plt
import numpy as np
from scipy import spatial
import argparse
import glob
import cv2
import csv

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", default='index.csv',
                help="Path to where the computed index will be stored")
ap.add_argument("-l", "--limit", default=10,
                help="Query result limit")
ap.add_argument("-v", "--vocabulary", default='vocabulary.npy',
                help="Path to where the computed vocabulary will be stored")
ap.add_argument("-d", "--dist", default='euclidean',
                help="Distance model")
ap.add_argument("-q", "--query", required=True,
                help="Path to the query image")
args = vars(ap.parse_args())


# initialize
sift = cv2.xfeatures2d.SIFT_create()
extract = sift
flann_params = dict(algorithm=1, trees=5)  # FLANN_INDEX_KDTREE=1
matcher = cv2.FlannBasedMatcher(flann_params, {})
bow_extractor = cv2.BOWImgDescriptorExtractor(extract, matcher)
voc = np.load(args['vocabulary'])
bow_extractor.setVocabulary(voc)

limit = int(args['limit'])


def euclidean_dist(a, b):
    return spatial.distance.euclidean(a, b)


def hamming_dist(a, b):
    return spatial.distance.hamming(a, b)


def cosine_dist(a, b):
    return spatial.distance.cosine(a, b)


dist_model = {
    'hamming': hamming_dist,
    'euclidean': euclidean_dist,
    'cosine': cosine_dist
}
dist = dist_model[args['dist']]


def bow(name):
    img = cv2.imread(name)
    return bow_extractor.compute(img, sift.detect(img))[0]


query_features = bow(args['query'])

results = {}
with open(args['index']) as f:
    # initialize the CSV reader
    reader = csv.reader(f)
    # loop over the rows in the index
    for row in reader:
        features = [float(x) for x in row[1:]]
        d = dist(features, query_features)

        results[row[0]] = d

    f.close()

results = sorted([(v, k) for (k, v) in results.items()])[:limit]

for (score, image_path) in results:
    # load the result image and display it
    print image_path
