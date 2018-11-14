import cv2
import os
import shutil


def show_bounding_box(file_name):

    f = open('./newlabel/' + file_name)
    str_bboxs = f.readlines()

    img_file_name = file_name[:-3] + 'jpg'
    dir = './newdata/'
    img = cv2.imread(dir + img_file_name)

    for str_bbox in str_bboxs:

        str_bbox = str_bbox[:-2]
        new_bbox = str_bbox.split(' ')

        x_min = int(new_bbox[0])
        y_min = int(new_bbox[1])
        x_max = int(new_bbox[2])
        y_max = int(new_bbox[3])
        img = cv2.rectangle(img, (x_min, y_min ),(x_max, y_max), 0xf00)
    print img_file_name
    cv2.imshow(img_file_name, img)


def copy_label_list_image(file):
    f = open(file)
    image_pathes = f.readlines()
    print image_pathes
    for image_path in image_pathes:
        img = cv2.imread(image_path[:-1])
        dir = './test_image/'
        if os.path.exists(dir) == False:
            os.makedirs(dir)
        cv2.imwrite(dir + image_path.split('/')[-1], img)


def copy_all_file_inderictory(dir):
    for roots, dirs, files in os.walk(dir):

        i = 0
        for file in files :
            i = i+1
            shutil.copy(dir+file, dir+'000{}.jpg'.format(i))


if __name__ == '__main__':
    new_label = './newlabel/'
    for root , dirs, files in os.walk(new_label):
        print files
        i =0
        for file in files:
            show_bounding_box(file)
            i +=1
            cv2.waitKey(1000)
    cv2.waitKey(0)
    # copy_label_list_image('val.txt')
    # copy_all_file_inderictory('./test_image/')
