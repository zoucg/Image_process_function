# _*_ encoding:utf-8 _*_
import cv2
import sys
import os
import re
import argparse
import numpy as np
from skimage.io import imread, imsave
import skimage

class ImageProcess(object):
    def __init__(self, source_image_dir=None, dest_image_dir=None):
        self.source_dir = source_image_dir
        self.des_dir = dest_image_dir
        self.total_count = 0

    def get_all_images(self):
        images = os.listdir(self.source_dir)
        images = [image for image in images if (image.endswith('jpg') or image.endswith('tif') or image.endswith('png'))]

        if len(images)==0:
            print('There is no images in source_dir')

        return images

    def os_walk_images(self, root_dir, expected_save_dir):
        i = 0
        relative_paths = []
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                # print(file)
                if (file.endswith('tif') or file.endswith('jpg') or file.endswith('png')):
                    if file.split('_')[-1][:-4] in ['17', '18', '19']:
                        level = file.split('_')[-1][:-4]
                        relative_path = os.path.join(root, file)
                        i += 1
                        # if i<=264:
                        #     continue
                        print(i, relative_path)
                        try:
                            self.crop_image(relative_path, 1024, 1024, 256, i, level, expected_save_dir)
                        except MemoryError:
                            pass
                        continue


        print(len(relative_paths))

    def crop_image(self, image_path,  expected_height, expected_width, over_lap, i, level, expected_save_dir):
        """
        this methord can oswalk all images in a root dir
        :param image_path:
        :param expected_height:
        :param expected_width:
        :param over_lap:
        :param i:
        :param level:
        :param expected_save_dir:
        :return:
        """

        # image_data = imread(image_path)
        image_data = cv2.imread(image_path)
        image_height = image_data.shape[0]
        image_width = image_data.shape[1]

        subimage_height_step = expected_height - over_lap
        subimage_width_step = expected_width - over_lap

        subimage_count = 0

        for start_h in range(0, image_height, subimage_height_step):
            for start_w in range(0, image_width, subimage_width_step):
                start_h_new = start_h
                start_w_new = start_w
                if start_h + expected_height > image_height:
                    start_h_new = image_height - expected_height
                if start_w + expected_width > image_width:
                    start_w_new = image_width - expected_width
                top_left_row = max(start_h_new, 0)
                top_left_col = max(start_w_new, 0)
                bottom_right_row = min(start_h + expected_height, image_height)
                bottom_right_col = min(start_w + expected_width, image_width)
                subimage = image_data[top_left_row:bottom_right_row, top_left_col: bottom_right_col, :]

                image_name = '{0:0=5}_{1:0=3}_{2:0=4}_{3}.{4}'.format(self.total_count, i, subimage_count, level, 'png')
                print(image_name)

                self.total_count += 1
                subimage_count += 1

                sub_dir = str(self.total_count // 8000)

                last_dir = os.path.join(expected_save_dir, sub_dir)
                if os.path.exists(last_dir) is False:
                    os.makedirs(last_dir)
                image_path = os.path.join(last_dir, image_name)
                # imsave(image_path, subimage)
                cv2.imwrite(image_path, subimage)

    def crop(self, images, expected_height, expected_width, over_lap):
        """
        this method crop images in a list
        :param images:
        :param expected_height:
        :param expected_width:
        :param over_lap:
        :return:
        """
        for image in images:
            image_path = os.path.join(self.source_dir, image)

            image_data = imread(image_path)
            image_height = image_data.shape[0]
            image_width = image_data.shape[1]

            subimage_height_step = expected_height - over_lap
            subimage_width_step = expected_width - over_lap

            for start_h in range(0, image_height, subimage_height_step):
                for start_w in range(0, image_width, subimage_width_step):
                    start_h_new = start_h
                    start_w_new = start_w
                    if start_h + expected_height > image_height:
                        start_h_new = image_height - expected_height
                    if start_w + expected_width > image_width:
                        start_w_new = image_width - expected_width
                    top_left_row = max(start_h_new, 0)
                    top_left_col = max(start_w_new, 0)
                    bottom_right_row = min(start_h + expected_height, image_height)
                    bottom_right_col = min(start_w + expected_width, image_width)
                    subimage = image_data[top_left_row:bottom_right_row, top_left_col: bottom_right_col, :]

                    subimage_name = 'subimg_{}_{}_{}_{}_{}.{}'.format\
                        (top_left_col, top_left_row, expected_width, expected_height, 0, 'jpg')

                    subimage_dir = os.path.join(self.des_dir, image[:-4])
                    if os.path.exists(subimage_dir) is False:
                        os.makedirs(subimage_dir)
                    subimage_path = os.path.join(subimage_dir, subimage_name)
                    imsave(subimage_path, subimage)




if __name__=="__main__":

    my_data = ImageProcess('/home/zoucg/new_hhd', '/home/zoucg/new_hhd')
    # my_data.os_walk_images('/home/zoucg/new_hhd/ship', '/home/zoucg/new_hhd/sub_images_out' )





