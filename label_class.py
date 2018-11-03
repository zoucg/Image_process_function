# python2.7
import os
import cv2
import xml.dom.minidom
import numpy as np
import copy


class Dataset(object):
    def __init__(self, source_image_dir, source_label_dir, dest_label_dir=None):
        if os.path.exists(dest_label_dir) is False:
            os.makedirs(dest_label_dir)

        self.source_image_dir = source_image_dir
        self.source_label_dir = source_label_dir
        self.dest_label_dir = dest_label_dir
        # self.class_list = ['plane', 'baseball-diamond', 'bridge', 'ground-track-field',
        #                    'small-vehicle', 'large-vehicle', 'ship', 'tennis-court',
        #                    'basketball-court',  'storage-tank', 'soccer-ball-field',
        #                    'roundabout', 'harbor', 'swimming-pool', 'helicopter']
        self.class_list = ['ship']

    def crop(self, new_image_dir, new_voc_dir):
        if os.path.exists(new_image_dir) is False:
            os.makedirs(new_image_dir)

        if os.path.exists(new_voc_dir) is False:
            os.makedirs(new_voc_dir)

        images = os.listdir(self.source_image_dir)
        images = [image for image in images if image.endswith('png')]
        flag = 0
        for im in images:
            print(im)
            flag += 1
            # if flag > 20:
            #     break
            print('crop{}'.format(im))
            label_path = os.path.join(self.source_label_dir, im[:-3]+'txt')
            object_list = self.get_label(label_path)
            self.crop_image_and_bbox(im, 1024, 1024, 256, object_list, new_image_dir, new_voc_dir)

    def txt2voc(self):
        """
        txt label change to xml label
        :return:
        """
        label_files = os.listdir(self.source_label_dir)

        for label_file in label_files:
            if label_file.endswith('txt'):

                label_file_path = os.path.join(self.source_label_dir, label_file)
                print(label_file_path)
                object_list = self.get_label(label_file_path)
                print object_list
                xml_file_name = label_file[:-3] + 'xml'
                self.creat_xml(xml_file_name, object_list)

    def get_label(self, label_file_path):
        """
        get all_objects in a image
        and generate a dict
        :param label_file_path:
        :return:[dict1, dict2, dicti]
        """
        object_list = []

        with open(label_file_path, 'rb') as lf:
            objects = lf.readlines()
            for object in objects:
                print((object.split(' ')[1]))
                object_dict = {}
                if len(object.split(' '))==11:
                    object_bbox = object.split(' ')[1:9]
                    object_name = object.split(' ')[9]
                    object_class = object.split(' ')[10][:-2]
                    print(object_class)
                    object_dict['object_box'] = object_bbox
                    object_dict['object_name'] = object_name
                    object_dict['object_class'] = self.class_list.index(object_name)
                    object_list.append(object_dict)
        return object_list

    def change_object_list_to_np_array(self, object_list):
        object_array = []
        for b in object_list:
            evey_box = [int(xy) for xy in b['object_box']] + [int(b['object_class'])]
            object_array.append(evey_box)
        object_np = np.array(object_array)
        return object_np

    def change_np_array_to_object_list(self, object_np):
        object_list = []
        for li in object_np:
            li = li.tolist()
            # array to list and num to str
            li = [str(l) for l in li]
            object_dict = {}
            object_dict['object_box'] = li[0:8]
            object_dict['object_class'] = li[-1]
            object_dict['object_name'] = self.class_list[int(li[-1])]

            object_list.append(object_dict)
        return object_list

    def crop_image_and_bbox(self, image_name, width, height, overlap, object_list, sub_image_dir, sub_label_dir):
        image_path = os.path.join(self.source_image_dir, image_name)
        image_np = cv2.imread(image_path)
        image_shape = image_np.shape
        image_height = image_shape[0]
        image_width = image_shape[1]
        sub_image_step = width - overlap
        if len(object_list)==0:
            return
        object_np = self.change_object_list_to_np_array(object_list)
        print('object:np', object_np)

        for start_h in range(0, image_height, sub_image_step):
            for start_w in range(0, image_width, sub_image_step):

                start_h_new = start_h
                start_w_new = start_w
                if start_h + height > image_height:
                    start_h_new = image_height - height
                if start_w + width > image_width:
                    start_w_new = image_width - width
                top_left_row = max(start_h_new, 0)
                top_left_col = max(start_w_new, 0)
                bottom_right_row = min(start_h + height, image_shape[0])
                bottom_right_col = min(start_w + width, image_shape[1])
                subimage = image_np[top_left_row:bottom_right_row, top_left_col: bottom_right_col, :]

                boxes = copy.deepcopy(object_np)
                box = np.zeros_like(object_np)

                # compute the centure of box , if the centure is in the subimage ,fetech

                box[:, 0] = boxes[:, 0] - top_left_col
                box[:, 2] = boxes[:, 2] - top_left_col
                box[:, 4] = boxes[:, 4] - top_left_col
                box[:, 6] = boxes[:, 6] - top_left_col

                box[:, 1] = boxes[:, 1] - top_left_row
                box[:, 3] = boxes[:, 3] - top_left_row
                box[:, 5] = boxes[:, 5] - top_left_row
                box[:, 7] = boxes[:, 7] - top_left_row
                box[:, 8] = boxes[:, 8]
                center_y = 0.25 * (box[:, 1] + box[:, 3] + box[:, 5] + box[:, 7])
                center_x = 0.25 * (box[:, 0] + box[:, 2] + box[:, 4] + box[:, 6])

                cond1 = np.intersect1d(np.where(center_y[:] >= 0)[0], np.where(center_x[:] >= 0)[0])
                cond2 = np.intersect1d(np.where(center_y[:] <= (bottom_right_row - top_left_row))[0],
                                       np.where(center_x[:] <= (bottom_right_col - top_left_col))[0])

                idx = np.intersect1d(cond1, cond2)

                if len(idx) > 0:
                    if subimage.shape[0] > 5 and subimage.shape[1] > 5:
                        img = os.path.join(sub_image_dir,"%s_%04d_%04d.png" % (image_name[:-4],
                                                                               top_left_row, top_left_col))
                        cv2.imwrite(img, subimage)

                    xml_file_name = "%s_%04d_%04d.xml" % (image_name[:-4], top_left_row, top_left_col)
                    # print(xml)
                    object_box = self.change_np_array_to_object_list(box[idx, :])
                    self.creat_xml(xml_file_name, object_box, sub_image_dir, sub_label_dir)

    def creat_xml(self, xml_file_name, object_list, sub_image_dir=None, sub_label_dir=None):
        if sub_label_dir is None:
            xml_file_path = os.path.join(self.dest_label_dir, xml_file_name)
        else:
            xml_file_path = os.path.join(sub_label_dir, xml_file_name)

        if sub_image_dir is None:
            image_file_path = os.path.join(self.source_image_dir, xml_file_name[:-3]+'png')
        else:
            image_file_path = os.path.join(sub_image_dir,  xml_file_name[:-3]+'png')
        print(image_file_path)

        if cv2.imread(image_file_path) is None:
            return
        image_shape = cv2.imread(image_file_path).shape

        doc = xml.dom.minidom.Document()
        root = doc.createElement('anotation')
        doc.appendChild(root)

        node_floder = doc.createElement('folder')
        node_floder.appendChild(doc.createTextNode('VOC2007'))

        node_filename = doc.createElement('filename')
        node_filename.appendChild(doc.createTextNode(xml_file_name[:-3] + 'jpg'))

        node_source = doc.createElement('source')
        node_database = doc.createElement('database')
        node_database.appendChild(doc.createTextNode('The VOC2007 Dotadataset'))
        node_anotation = doc.createElement('anotation')
        node_anotation.appendChild(doc.createTextNode('PASCAL VOC2007'))
        node_image = doc.createElement('image')
        node_image.appendChild(doc.createTextNode('fickrid'))
        node_fickrid = doc.createElement('fickrid')
        node_fickrid.appendChild(doc.createTextNode('341012865'))

        node_source.appendChild(node_database)
        node_source.appendChild(node_anotation)
        node_source.appendChild(node_image)
        node_source.appendChild(node_fickrid)

        node_ownner = doc.createElement('ownner')
        node_frick = doc.createElement('fickrid')
        node_frick.appendChild(doc.createTextNode('zoucg'))
        node_name = doc.createElement('name')
        node_name.appendChild(doc.createTextNode('zoucg'))
        node_ownner.appendChild(node_fickrid)
        node_ownner.appendChild(node_name)

        node_size = doc.createElement('size')
        node_width = doc.createElement('width')
        node_width.appendChild(doc.createTextNode(str(image_shape[0])))
        node_height = doc.createElement('height')
        node_height.appendChild(doc.createTextNode(str(image_shape[1])))
        node_depth = doc.createElement('depth')
        node_depth.appendChild(doc.createTextNode(str(image_shape[2])))
        node_size.appendChild(node_width)
        node_size.appendChild(node_height)
        node_size.appendChild(node_depth)

        node_segment = doc.createElement('segmented')
        node_segment.appendChild(doc.createTextNode('0'))

        root.appendChild(node_floder)
        root.appendChild(node_filename)
        root.appendChild(node_source)
        root.appendChild(node_ownner)
        root.appendChild(node_size)
        root.appendChild(node_segment)

        for b in object_list:
            print(b)
            node_object = doc.createElement('object')

            node_name1 = doc.createElement('name')
            node_name1.appendChild(doc.createTextNode(b['object_name']))
            node_pose = doc.createElement('pose')
            node_pose.appendChild(doc.createTextNode('left'))
            node_truncated = doc.createElement('truncated')
            node_truncated.appendChild(doc.createTextNode('0'))
            node_diffcult = doc.createElement('difficult')
            node_diffcult.appendChild(doc.createTextNode('0'))

            node_bndbox = doc.createElement('bndbox')
            node_x0 = doc.createElement('x0')
            node_x0.appendChild(doc.createTextNode(b['object_box'][0]))
            node_y0 = doc.createElement('y0')
            node_y0.appendChild(doc.createTextNode(b['object_box'][1]))
            node_x1 = doc.createElement('x1')
            node_x1.appendChild(doc.createTextNode(b['object_box'][2]))
            node_y1 = doc.createElement('y1')
            node_y1.appendChild(doc.createTextNode(b['object_box'][3]))
            node_x2 = doc.createElement('x2')
            node_x2.appendChild(doc.createTextNode(b['object_box'][4]))
            node_y2 = doc.createElement('y2')
            node_y2.appendChild(doc.createTextNode(b['object_box'][5]))
            node_x3 = doc.createElement('x3')
            node_x3.appendChild(doc.createTextNode(b['object_box'][6]))
            node_y3 = doc.createElement('y3')
            node_y3.appendChild(doc.createTextNode(b['object_box'][7]))
            node_bndbox.appendChild(node_x0)
            node_bndbox.appendChild(node_y0)
            node_bndbox.appendChild(node_x1)
            node_bndbox.appendChild(node_y1)
            node_bndbox.appendChild(node_x2)
            node_bndbox.appendChild(node_y2)
            node_bndbox.appendChild(node_x3)
            node_bndbox.appendChild(node_y3)

            node_object.appendChild(node_name1)
            node_object.appendChild(node_pose)
            node_object.appendChild(node_truncated)
            node_object.appendChild(node_diffcult)
            node_object.appendChild(node_bndbox)

            root.appendChild(node_object)

        with open(xml_file_path, 'wb') as xf:
            doc.writexml(xf, indent='\t', addindent='\t', newl='\n', encoding="utf-8")

def main():
    # source_image_dir = '/home/zoucg/new_disk/cv_project/tensorflow_project' \
    #                    '/R2CNN_Faster-RCNN_Tensorflow/dataset/DOTA/train/images'
    # source_label_dir = '/home/zoucg/new_disk/cv_project/tensorflow_project/' \
    #                    'R2CNN_Faster-RCNN_Tensorflow/dataset/DOTA/train/labelTxt'

    source_image_dir = '/home/zoucg/new_hhd/LABELED_SHIP/slected/ALL/all'
    source_label_dir = '/home/zoucg/new_hhd/LABELED_SHIP/slected/ALL/txt'
    dota = Dataset(source_image_dir, source_label_dir, '/home/zoucg/new_hhd/LABELED_SHIP/slected/ALL/Annotations')
    # dota.crop('./val_JPEGimages', './val_Annotation_all')
    dota.txt2voc()

if __name__ =='__main__':
  main()