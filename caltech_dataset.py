import PIL.Image
from torchvision.datasets import VisionDataset
import numpy as np
from PIL import Image

import os
import os.path
import sys


def pil_loader(path):
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        with Image.open(f) as img:
            return img.convert('RGB')


class Caltech(VisionDataset):
    def __init__(self, root, split='train', transform=None, target_transform=None):
        super(Caltech, self).__init__(root, transform=transform, target_transform=target_transform)

        self.split = split # This defines the split you are going to use
                           # (split files are called 'train.txt' and 'test.txt')

        '''
        - Here you should implement the logic for reading the splits files and accessing elements
        - If the RAM size allows it, it is faster to store all data in memory
        - PyTorch Dataset classes use indexes to read elements
        - You should provide a way for the __getitem__ method to access the image-label pair
          through the index
        - Labels should start from 0, so for Caltech you will have lables 0...100 (excluding the background class) 
        
        '''
        path = split + '.txt'
        data_x = []
        data_y = []
        parent = root.split('/')[0]
        label_encoder = np.load(parent + '/' + 'label_encoder.npy')
        with open(parent + '/' + path) as f:
            lines = f.readlines()
            for line in lines:
                if 'BACKGROUND' in line:
                    continue
                line = line.strip('\n')
                img = pil_loader(root + '/' + line)
                data_x.append(transform(img) if transform else img)
                data_y.append(np.where(label_encoder == (line.split('/')[0]))[0][0])

        ids = np.array(range(0, len(data_x)))
        np.random.shuffle(ids)
        data_x = np.array(data_x)
        data_y = np.array(data_y)
        self.data_x = data_x[ids]
        self.data_y = data_y[ids]


    def __getitem__(self, index):
        '''
        __getitem__ should access an element through its index
        Args:
            index (int): Index

        Returns:
            tuple: (sample, target) where target is class_index of the target class.
        '''
        if index > self.data_x.shape[0]:
            raise IndexError('Index out of range')

        image, label = self.data_x[index], self.data_y[index] # Provide a way to access image and label via index
                           # Image should be a PIL Image
                           # label can be int

        # Applies preprocessing when accessing the image
        if self.transform is not None:
            image = self.transform(image)

        return image, label

    def __len__(self):
        '''
        The __len__ method returns the length of the dataset
        It is mandatory, as this is used by several other components
        '''
        length = self.data_x.shape[0] # Provide a way to get the length (number of elements) of the dataset
        return length

    def get_data(self):
        return self.data_x, self.data_y
