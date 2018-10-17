# _*_encoding:utf-8 _*_
import os
import xml.dom.minidom
import change_label_mode
import cv2
import random

def read_txt(file_name):
    f = open(file_name)
    new_boundingbox = []
    bounding_box = f.readlines()
    f.close()
    for b in bounding_box:
        b = b[:-2]
        new_boundingbox.append(b)
    return new_boundingbox


def creat_xml(boudngingbox, file):
    # get the imge shape
    dir_name = './newdata/'
    jpg_file_path = dir_name+file[:-3]+'jpg'
    # print jpg_file_path
    img = cv2.imread(jpg_file_path)
    datashape = img.shape
    # print datashape
    # datashape = [450, 450, 3]

    doc = xml.dom.minidom.Document()
    root = doc.createElement('anotation')
    doc.appendChild(root)

    node_floder = doc.createElement('folder')
    node_floder.appendChild(doc.createTextNode('VOC2007'))

    node_filename = doc.createElement('filename')
    node_filename.appendChild(doc.createTextNode(file[:-3]+'jpg'))

    node_source = doc.createElement('source')
    node_database = doc.createElement('database')
    node_database.appendChild(doc.createTextNode('The VOC2007 Database'))
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
    node_width.appendChild(doc.createTextNode(str(datashape[0])))
    node_height = doc.createElement('height')
    node_height.appendChild(doc.createTextNode(str(datashape[1])))
    node_depth = doc.createElement('depth')
    node_depth.appendChild(doc.createTextNode(str(datashape[2])))
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

    for b in boudngingbox:
        node_object = doc.createElement('object')

        node_name1 = doc.createElement('name')
        node_name1.appendChild(doc.createTextNode('sonar'))
        node_pose = doc.createElement('pose')
        node_pose.appendChild(doc.createTextNode('left'))
        node_truncated = doc.createElement('truncated')
        node_truncated.appendChild(doc.createTextNode('0'))
        node_diffcult = doc.createElement('difficult')
        node_diffcult.appendChild(doc.createTextNode('0'))

        node_bndbox = doc.createElement('bndbox')
        node_xmin = doc.createElement('xmin')
        node_xmin.appendChild(doc.createTextNode(b.split(' ')[0]))
        node_ymin = doc.createElement('ymin')
        node_ymin.appendChild(doc.createTextNode(b.split(' ')[1]))
        node_xmax = doc.createElement('xmax')
        node_xmax.appendChild(doc.createTextNode(b.split(' ')[2]))
        node_ymax = doc.createElement('ymax')
        node_ymax.appendChild(doc.createTextNode(b.split(' ')[3]))
        node_bndbox.appendChild(node_xmin)
        node_bndbox.appendChild(node_ymin)
        node_bndbox.appendChild(node_xmax)
        node_bndbox.appendChild(node_ymax)

        node_object.appendChild(node_name1)
        node_object.appendChild(node_pose)
        node_object.appendChild(node_truncated)
        node_object.appendChild(node_diffcult)
        node_object.appendChild(node_bndbox)

        root.appendChild(node_object)

    dir = './new_voc/anotation/'
    if os.path.exists(dir) is not True:
        os.makedirs(dir)

    xml_file = dir + file[:-3] + 'xml'
    f = open(xml_file, "w+")
    doc.writexml(f,indent='\t', addindent='\t', newl='\n', encoding="utf-8")


def make_list(dir_name,dest_dir):
    jpg_files = []
    files = os.listdir(dir_name)
    for file in files:
        if file.endswith('jpg'):
            jpg_files.append(file)
    jpg_files.sort()
    fs = random.sample(jpg_files,15)

    # print jpg_files

    test_list = fs
    all_files = jpg_files
    for t in test_list:
        jpg_files.remove(t)
    train_list = jpg_files
    new_test_list = []
    new_train_list = []
    for te in test_list:
        new_test_list.append(te[:-4]+ '\r\n')
    for tr in train_list:
        new_train_list.append(tr[:-4]+'\r\n')

    new_train_list.sort()
    new_test_list.sort()
    print new_train_list
    print new_test_list

    if os.path.exists(dest_dir) is False:
        os.makedirs(dest_dir)
    f = open(dest_dir + 'trainval.txt', 'w+')
    f.writelines(new_train_list)
    f2 = open(dest_dir + 'test.txt', 'w+')
    f2.writelines(new_test_list)




def main():
    # all_files = change_label_mode.get_all_files('./newlabel/')
    # dir = './newlabel/'
    #
    # for file in all_files:
    #     txt_file = file[-2]
    #     bb = read_txt(dir + txt_file)
    #     creat_xml(bb, txt_file)
    # make_test('val.txt')
    # make_test('train.txt')
    make_list('./newdata/','./new_voc/ImageSets/Main/')


if __name__ == '__main__':
    main()
    # t = random.randint(0,98)
    # print t

