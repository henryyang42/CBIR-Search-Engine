import numpy as np
import argparse
import glob
import time
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", default='dataset',
                help="Path to the directory that contains the images to be indexed")  # noqa
ap.add_argument("-v", "--vocabulary", default='vocabulary',
                help="Path to where the computed vocabulary will be stored")
ap.add_argument("-vc", "--vocabulary_size", default=64,
                help="Vocabulary size")
args = vars(ap.parse_args())

start = time.time()

bow_trainer = cv2.BOWKMeansTrainer(int(args['vocabulary_size']))
sift = cv2.xfeatures2d.SIFT_create()

for imagePath in glob.glob(args["dataset"] + "/*.*g"):
    img = cv2.imread(imagePath)

    kp, des = sift.detectAndCompute(img, None)
    bow_trainer.add(des)
    print imagePath

print '\nClustering %d descriptors...' % bow_trainer.descriptorsCount()
voc = bow_trainer.cluster()

print "BoW vocabulary size = ", np.shape(voc)
np.save(args['vocabulary'], voc)

print 'Time = %s' % (time.time()-start)
