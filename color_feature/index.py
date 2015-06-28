# USAGE
# python index.py --dataset dataset --index index.csv

# import the necessary packages
from colordescriptor import ColorDescriptor
import progressbar
import argparse
import glob
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", default='dataset',
                help="Path to the directory that contains the images to be indexed")  # noqa
ap.add_argument("-i", "--index", default='index.csv',
                help="Path to where the computed index will be stored")
args = vars(ap.parse_args())

# initialize the color descriptor
cd = ColorDescriptor((8, 12, 3))

# open the output index file for writing
output = open(args["index"], "w")

pb = progressbar.ProgressBar()
# use glob to grab the image paths and loop over them
for imagePath in pb(glob.glob(args["dataset"] + "/*.*g")):
    # extract the image ID (i.e. the unique filename) from the image
    # path and load the image itself
    image = cv2.imread(imagePath)

    # describe the image
    features = cd.describe(image)

    # write the features to file
    features = [str(f) for f in features]
    output.write("%s,%s\n" % (imagePath, ",".join(features)))

# close the index file
output.close()
