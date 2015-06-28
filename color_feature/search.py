# USAGE
# python search.py --index index.csv --query queries/103100.png
# --result-path dataset

# import the necessary packages
from colordescriptor import ColorDescriptor
from searcher import Searcher
import argparse
import cv2
import time
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", default='index.csv',
                help="Path to where the computed index will be stored")
ap.add_argument("-l", "--limit", default=10,
                help="Query result limit")
ap.add_argument("-q", "--query", required=True,
                help="Path to the query image")
args = vars(ap.parse_args())

# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))

# load the query image and describe it
query = cv2.imread(args["query"])
features = cd.describe(query)

# perform the search
searcher = Searcher(args["index"])
results = searcher.search(features, int(args["limit"]))

# loop over the results
for (score, resultID) in results:
    # load the result image and display it
    print resultID
