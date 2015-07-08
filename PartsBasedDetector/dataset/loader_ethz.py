from glob import glob
import os
import csv
from subprocess import call
import shutil

import numpy as np
from scipy.misc import imread, imsave

from util import download, untar, unzip


dataset_root = os.path.dirname(os.path.abspath(__file__))

class ETHZDatasetPreparer(object):
    def __init__(self):
        url = \
            'http://groups.inf.ed.ac.uk/calvin/ethz_pascal_stickmen/'\
            'downloads/ETHZ_PASCAL_Stickmen_v1.11.tgz'
        data_filename = os.path.basename(url)
        self.data_filepath = os.path.join(dataset_root,
                                          data_filename)
        data_directory = os.path.join(dataset_root,
                                           'ETHZ_PASCAL_Stickmen_v1.11')
        self.loaded = False

        if not(os.path.exists(self.data_filepath)):
            download(url, self.data_filepath)

        if not(os.path.exists(data_directory)):
            untar(self.data_filepath, dataset_root)

            shutil.move(os.path.join(data_directory, 'images'),
                        os.path.join(dataset_root, 'images'))

            shutil.move(os.path.join(data_directory, 'data'),
                        os.path.join(dataset_root, 'annotations'))

    def load(self):
        filenames = []

        # the coordinates of body parts in an image
        # should be represented like below
        # [x1 y1]
        # [x2 y2]
        # ...
        # [x6 y6]

        coordinates = []
        images = []
        image_path_template = os.path.join(dataset_root,
                                           'images',
                                           '{:>06}')

        t = os.path.join(dataset_root, 'annotations',
                         'pascal_sticks.txt')
        for row in csv.reader(open(t, 'r'), delimiter=' '):
            if(len(row) == 1):
                n_rows = 0
                points = []
                image_path = image_path_template.format(row[0])
                images.append(imread(image_path))
                continue

            points += list(map(float, row[1:5]))

            n_rows += 1
            if(n_rows == 6):
                points = np.array(points)
                x = points[::2]  #even elements indicate x positions
                x[2], x[3] = x[3], x[2]
                x[4], x[5] = x[5], x[4]
                x[6], x[7] = x[7], x[6]
                x[8], x[9] = x[9], x[8]
                y = points[1::2]  #odd elements indicate y positions
                y[2], y[3] = y[3], y[2]
                y[4], y[5] = y[5], y[4]
                y[6], y[7] = y[7], y[6]
                y[8], y[9] = y[9], y[8]
                coordinates.append(np.array([x, y]).T)

        self.coordinates = coordinates
        self.images = images
        self.loaded = True

    def export(self, dataset_directory):
        if not(self.loaded):
            raise AssertionError('Data not loaded.')

        if not(os.path.exists(dataset_directory)):
            os.makedirs(dataset_directory)

        for i in range(len(self.images)):
            filename = '{:>06}.jpg'.format(i)
            path = os.path.join(dataset_directory, filename)
            imsave(path, self.images[i])

            filename = '{:>06}.txt'.format(i)
            path = os.path.join(dataset_directory, filename)
            writer = csv.writer(open(path, 'w'))
            writer.writerows(self.coordinates[i].tolist())

    def plot_overlayed(self, index):
        n_images = len(self.images)
        if(index >= n_images):
            m = "Object contains only {} images. "\
                "Index too large.".format(n_images)
            raise ValueError(m)

        import matplotlib.pyplot as plt
        plt.imshow(self.images[index])
        plt.scatter(*self.coordinates[index].T)
        for i, coordinate in enumerate(self.coordinates[index]):
            plt.annotate(i+1, coordinate, color='white')

        plt.show()


def prepare_negative_dataset(dataset_directory):
    negative_dataset_url = \
        'http://www.ics.uci.edu/~dramanan/papers/parse/people.zip'
    data_filepath = os.path.join(dataset_root,
                                 os.path.basename(negative_dataset_url))
    if not(os.path.exists(data_filepath)):
        download(negative_dataset_url, path=data_filepath)
    unzip(data_filepath, dataset_root)

    shutil.move(os.path.join(dataset_root, 'people_all'), dataset_directory)


loader = ETHZDatasetPreparer()
loader.load()
dataset_directory = os.path.join(dataset_root, 'positive')
loader.export(dataset_directory=dataset_directory)

dataset_directory = os.path.join(dataset_root, 'negative')
prepare_negative_dataset(dataset_directory=dataset_directory)
