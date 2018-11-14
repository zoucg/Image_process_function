import numpy as np
import cv2
import os

class ResultsManger(object):
    def __init__(self, source_img_dir, source_labe_dir):
        self.source_img_dir = source_img_dir
        self.source_label_dir = source_labe_dir

    def prase_result_file(self, file_path):
        with open(file_path, 'r') as f:
            objectlist = f.readlines()
            print(objectlist)
            if len(objectlist)==0:
                return

            objectlist = objectlist[:-1]
            points_list = []
            for object in objectlist:
                object = object.split(' ')
                print(object)
                p0 = [int(object[1]), int(object[2])]
                p1 = [int(object[3]), int(object[4])]
                p2 = [int(object[5]), int(object[6])]
                p3 = [int(object[7]), int(object[8])]
                object = [p0, p1, p2, p3]
                points_list.append(object)

        return points_list


    def draw_object(self, object_list, img_path):
        img = cv2.imread(img_path)

        for object in object_list:
            pts = np.array(object, np.int32)
            pts = pts.reshape(-1, 1, 2)
            img = cv2.polylines(img,[pts], True,(255,255, 0),3)
        return img

    def get_out_results(self, dest_dir):
        if os.path.exists(dest_dir) is False:
            os.makedirs(dest_dir)
        labels = os.listdir(self.source_label_dir)
        labels = (label for label in labels if label.endswith('txt'))

        for i, label in enumerate(labels):
            print(label)
            label_path = os.path.join(self.source_label_dir, label)
            points_list = self.prase_result_file(label_path)
            img_name = label[:-3] + 'png'
            img_path = os.path.join(self.source_img_dir, img_name)
            img = self.draw_object(points_list, img_path)
            img_dest_path = os.path.join(dest_dir, img_name)
            cv2.imwrite(img_dest_path, img)
            if i > 10:
                break


def main():
    source_img_dir = '/home/zoucg/new_hhd/LABELED_SHIP/part0'
    source_label_dir = '/home/zoucg/new_hhd/LABELED_SHIP/part0'
    label_result = ResultsManger(source_img_dir, source_label_dir)
    label_result.get_out_results('/home/zoucg/new_hhd/label_check')

if __name__=='__main__':
    main()