import os
import cv2
import xml.dom.minidom

class Dataset(object):
    def __init__(self, source_image_dir, source_label_dir, dest_label_dir=None):
        if os.path.exists(dest_label_dir) is False:
            os.makedirs(dest_label_dir)

        self.source_image_dir = source_image_dir
        self.source_label_dir = source_label_dir
        self.dest_label_dir = dest_label_dir


    def txt2voc(self):
        label_files =  os.listdir(self.source_label_dir)

        for label_file in label_files:
            if label_file.endswith('txt'):

                label_file_path = os.path.join(self.source_label_dir, label_file)
                object_list = self.get_label(label_file_path)
                xml_file_name = label_file[:-3] + 'xml'
                self.creat_xml(xml_file_name, object_list)



    def get_label(self, label_file_path):
        """
        get all_objects in a image
        and generate a dict
        :param label_file_path:
        :return:
        """
        object_list = []

        with open(label_file_path, 'rb') as lf:
            objects = lf.readlines()
            for object in objects :
                object_dict = {}
                if len(object.split(' '))==10:
                    object_bbox = object.split(' ')[0:8]
                    object_name = object.split(' ')[8]
                    object_class = object.split(' ')[9][:-2]
                    object_dict['object_box'] = object_bbox
                    object_dict['object_name'] = object_name
                    object_dict['object_class'] = object_class
                    object_list.append(object_dict)
        return object_list

    def creat_xml(self, xml_file_name, object_list):
        xml_file_path = os.path.join(self.dest_label_dir, xml_file_name)
        image_file_path = os.path.join(self.source_image_dir, xml_file_name[:-3]+'png')
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
            node_x0= doc.createElement('x0')
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

if __name__ =='__main__':
    source_image_dir = '/home/zoucg/new_disk/cv_project/tensorflow_project/R2CNN_Faster-RCNN_Tensorflow/dataset/DOTA/train/images'
    source_label_dir = '/home/zoucg/new_disk/cv_project/tensorflow_project/R2CNN_Faster-RCNN_Tensorflow/dataset/DOTA/train/labelTxt'
    Dota = Dataset(source_image_dir, source_label_dir, './Annotation2')
    Dota.txt2voc()

