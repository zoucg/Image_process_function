#-*-coding:utf-8-*-
import os
import cv2
import shutil
import numpy as np
"""
test commit 
"""


def get_all_files(dir_name):
    label_path = dir_name
    all_labels = []

    for root, paths, files in os.walk(label_path):
        i = 0
        for file in  files:
            if file.endswith('txt'):
                f = open(root+file, 'r+')

                file_content = f.readlines()

                # labels_onefile = file_content.split("\r\n")
                boundingbox_num = len(file_content)
                # file_content.append(root+file)
                file_content.append(file)
                file_content.append(boundingbox_num)

                # file_content = ['0 0.373437 0.627083 0.112500 0.043056\r\n', './origdata/Survey0902241029001---obj.txt', 1]
                # print file_content

                all_labels.append(file_content)
    return all_labels


def prase_label(label):
    # for label in labels
    # class_id =
    boundingbox_num = label[-1]
    boundingbox = []
    if label[-1] > 0:
        for sub_label in label[0:boundingbox_num]:
            boundingbox.append(sub_label[:-2])

    file_name = label[-2]
    # boundingbox = ['0 0.751562 0.539583 0.142188 0.043056\r\n', '0 0.436328 0.394444 0.063281 0.038889\r\n']
    return boundingbox, file_name


def boundingbox_location_change(boundingbox, file_name, dir):
    root = dir
    jpgfile = file_name[0:-3]+'jpg'
    img = cv2.imread(root+jpgfile)
    shape = img.shape
    print (img.shape)
    print boundingbox
    new_boundingbox = []

    for b in boundingbox:
        axis = b.split(' ')
        x = float(axis[1])
        x = x * shape[0]
        y = float(axis[2])
        y = y*shape[1]
        width = float(axis[3])
        width = width * shape[0]
        heights = float(axis[4])
        heights = heights * shape[1]

        xmin = x - 0.5*width
        ymin = y - 0.5*heights
        xmax = x + 0.5*width
        ymax = y + 0.5*heights
        new_b = [int(xmin), int(ymin), int(xmax), int(ymax)]
        new_boundingbox.append(new_b)
    return new_boundingbox


def bbox_num2str(boundingbox):
    new_boundingbox = []
    for b in boundingbox:
        new_b = str(b[0]) + ' ' + str(b[1]) + ' ' + str(b[2]) + ' ' + str(b[3]) + '\r\n'
        new_boundingbox.append(new_b)
    return new_boundingbox


def write_label(boundingbox, file_name, dir):
    file_path = file_name
    root = dir
    if os.path.exists(root) is not True:
        os.makedirs(root)

    f = open(root+file_path, "w+")
    f.writelines(boundingbox)


def rename_file(dir_name,new_dir_name):
    if os.path.exists(new_dir_name) == False:
        os.makedirs(new_dir_name)
    for root, dir, files in os.walk(dir_name):
        old_file2new_file = []
        i = 0
        for file in files:
            # print file
            img_num = '0000' + str(i)
            img_num = img_num[-5:]
            new_file_name = 'sonar_'+img_num
            if file.endswith('jpg'):
                shutil.copy(dir_name+file, new_dir_name+new_file_name+'.jpg')
                shutil.copy(dir_name+file[:-3]+'txt', new_dir_name+new_file_name+'.txt')
                t = [file, new_file_name +'.jpg']
                old_file2new_file.append(t)
                print t
                i = i+1
                print i


def copy_files(src_dir, dest_dir,file_format='jpg'):
    if os.path.exists(dest_dir) is False:
        os.makedirs(dest_dir)
    files = os.listdir(src_dir)

    for fi in files:
        if fi.endswith(file_format):
            shutil.copy(src_dir+fi, dest_dir+fi)


def draw_label2jpg(label_file_dir,jpg_file_dir,new_label_img_dir):
    label_files = os.listdir(label_file_dir)
    if os.path.exists(new_label_img_dir) is False:
        os.makedirs(new_label_img_dir)
    for la_f in label_files:
        f = open(label_file_dir+la_f,'r+')
        labels = f.readlines()
        img_file =  la_f[:-3]+'jpg'
        im = cv2.imread(jpg_file_dir+img_file)
        for label in labels:
            xmin = label[:-2].split(' ')[0]
            ymin = label[:-2].split(' ')[1]
            xmax = label[:-2].split(' ')[2]
            ymax = label[:-2].split(' ')[3]
            cv2.rectangle(im, (int(xmin),int(ymin)),(int(xmax), int(ymax)), 0xf00)
        cv2.imwrite(new_label_img_dir+'labeled_'+img_file, im)


def copy_file_according_list(sorce_dir,dest_dir, list):
    if os.path.exists(dest_dir) is False:
        os.makedirs(dest_dir)
    f = open(list)
    names = f.readlines()
    for name in names:
        name = name[:-2]
        sorce_jpg_file = name+'.jpg'
        dest_file = name+ '.jpg'
        shutil.copy(sorce_dir+sorce_jpg_file, dest_dir+dest_file )



def main():
    all_label = get_all_files('./newdata/')
    for i in xrange(len(all_label)):

        bbox, filename = prase_label(all_label[i])
        new = boundingbox_location_change(bbox, filename, './newdata/')
        str_bbox = bbox_num2str(new)
        write_label(str_bbox, filename, './newlabel/')

# def prase(dir,xml_file):
#     xml_file = os.path.join(dir, xml_file)
#     xml.dom.

if __name__ == "__main__":
    # main()
    # rename_file('./boxdata/', './newdata/')
    # copy_files('./newdata/', './new_voc/JPEGImages/')
    # draw_label2jpg('./newlabel/', './newdata/', './labeld_img/')
    # dest_dir = '/ home / zoucg / cv_project / caffe_project / py - faster - rcnn / demo_results /'
    # dest_dir = './test_img/'
    copy_file_according_list('./voc/JPEGImages/', './test/','./voc/ImageSets/Main/test.txt')
    # copy_files('./newdata/', './gandata/')
    # file = os.listdir('./wangxiang/')
    # i=0
    # file_num = len(file)
    # for f in file:
    #     if i<1350:
    #         shutil.copy('./wangxiang/' + f, './part1/' + f)
    #     elif i<2700:
    #         shutil.copy('./wangxiang/' + f, './part2/' + f)
    #     elif i<4050:
    #         shutil.copy('./wangxiang/' + f, './part3/' + f)
    #     else:
    #         shutil.copy('./wangxiang/' + f, './part4/' + f)
    #     i+=1
    # copy_files('./box-GF2-20180831/','./voc/Annotations/','xml')
