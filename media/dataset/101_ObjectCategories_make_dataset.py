import argparse
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", default='dataset',
                help="Path to the directory that contains the images to be indexed")  # noqa
ap.add_argument("-s", "--size", default=20,
                help="Size of each category")

limit = arg['limit']

for dirname, dirnames, filenames in os.walk('101_ObjectCategories'):
    for f in filenames[:limit]:
        ff = '%s/%s' % (dirname, f)
        os.system("cp %s %s/%s_%s" % (ff, mt, dirname, f))
