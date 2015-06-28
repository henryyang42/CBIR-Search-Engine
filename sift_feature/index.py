import numpy as np
import progressbar
import argparse
import glob
import time
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", default='dataset',
                help="Path to the directory that contains the images to be indexed")  # noqa
ap.add_argument("-v", "--vocabulary", default='vocabulary.npy',
                help="Path to where the computed vocabulary will be stored")
ap.add_argument("-i", "--index", default='index.csv',
                help="Path to where the computed index will be stored")
args = vars(ap.parse_args())

start = time.time()

# initialize
sift = cv2.xfeatures2d.SIFT_create()
extract = sift
flann_params = dict(algorithm=1, trees=5)  # FLANN_INDEX_KDTREE=1
matcher = cv2.FlannBasedMatcher(flann_params, {})
bow_extractor = cv2.BOWImgDescriptorExtractor(extract, matcher)
voc = np.load(args['vocabulary'])
bow_extractor.setVocabulary(voc)


# open the output index file for writing
output = open(args["index"], "w")

pb = progressbar.ProgressBar()
# use glob to grab the image paths and loop over them
for image_path in pb(glob.glob(args["dataset"] + "/*.*g")):
    # path and load the image itself
    image = cv2.imread(image_path)

    # describe the image
    features = bow_extractor.compute(image, sift.detect(image))[0]
    # write the features to file
    features = [str(f) for f in features]
    output.write("%s,%s\n" % (image_path, ",".join(features)))

# close the index file
output.close()

print 'Time = %s' % (time.time()-start)
