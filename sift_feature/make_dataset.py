import argparse
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", default='dataset',
                help="Path to the directory that contains the images to be indexed")  # noqa
ap.add_argument("-s", "--size", default=20,
                help="Size of each category")
args = vars(ap.parse_args())

limit = int(args['size'])
path = args['dataset']

os.mkdir(path)

for dirname, dirnames, filenames in os.walk('101_ObjectCategories'):
    for name in filenames[:min(limit, len(filenames))]:
        image_name = '%s/%s' % (dirname, name)
        folder_name = dirname.split('/')[-1]
        os.system("cp %s %s/%s_%s" % (image_name, path, folder_name, name))
