import shutil
import os
import re

class DataProcess(object):
    def __init__(self, source_dir, dest_dir):
        if os.path.exists(dest_dir) is False:
            os.makedirs(dest_dir)

        self.source_dir = source_dir
        self.dest_dir = dest_dir

    def get_all_flies(self, file_format, source_dir):
        file_dir = source_dir
        files = os.listdir(file_dir)
        files = [fi for fi in files if fi.endswith(file_format)]
        return files

    def choose_withobject(self, file_format):
        files = self.get_all_flies(file_format,self.source_dir)

        for fi in files:
            fi_path = os.path.join(self.source_dir, fi)
            with open(fi_path, 'r') as fi_p:
                if len(fi_p.readlines())> 0 and(self.is_right_label(fi_p)):

                    dest_path = os.path.join(self.dest_dir, fi)
                    print(dest_path)
                    source_path = os.path.join(self.source_dir, fi)
                    print(source_path)
                    shutil.copy(source_path, self.dest_dir)
                    shutil.copy(source_path[:-3] + 'png', self.dest_dir)

    def is_right_label(self,fp):
        lines = fp.readlines()
        for line in lines:
            if len(line.split(' ')) != 11:
                return False
        return True


def split_end(x):
    return x.split('/')[-1]


def allocate_file(soure_dir, dest_dir=None, num_sub_dir=None):
    """"""
    f = open('log.txt', 'w')
    path_list = []
    for root, dirs, files in os.walk(soure_dir):
        # print(files)
        for file in files:
            # print(file[-3:])
            if file[-3:]=='png':
                # print('hello')
                file_path = os.path.join(root, file)
                path_list.append(file_path)

    print(path_list)
    print(path_list[0])
    print('hello')
    path_list.sort(key=split_end)
    i = 0
    thresh_hold = len(path_list)//num_sub_dir

    cout = 0
    for i ,path in enumerate(path_list):
        if i<=18295:
            continue
        sub_dir = i//thresh_hold
        dest_path = os.path.join(dest_dir, str(sub_dir), path.split('/')[-1])
        if os.path.exists(os.path.join(dest_dir, str(sub_dir))) is False:
            os.makedirs(os.path.join(dest_dir, str(sub_dir)))
        shutil.copy(path, dest_path)
        print(i, path, file=f)
        print(i, path)


class LabeledDataManager(object):
    def __init__(self, source_dir, dest_dir):
        if os.path.exists(dest_dir) is False:
            os.makedirs(dest_dir)
        self.source_dir = source_dir
        self.dest_dir = dest_dir

    def selected_error(self, list_file):
        with open(list_file) as f:
            nums = f.readlines()

        names = os.listdir(self.source_dir)
        names = [name for name in names if name.endswith('txt')]
        print(nums)

        for num in nums:
            num = num[:-1]
            print(num)
            name = self.name_match(num, names)
            if name is not None:
                try:
                    label_path = os.path.join(self.source_dir, name)
                    img_path = os.path.join(self.source_dir, name[:-3] + 'png')
                    shutil.move(label_path, self.dest_dir)
                    shutil.move(img_path, self.dest_dir)
                except shutil.Error:
                    continue

    def name_match(self, num, names):
        for name in names:
            if re.match(num, name)is not None:
                print(num)
                return name

def main():
    source_dir = '/home/zoucg/new_hhd/exist_object/5'
    dest_dir = '/home/zoucg/new_hhd/exist_object/5_error'
    list_file = '/home/zoucg/Desktop/error_labeled_img5'
    # source_dir = '/home/zoucg/new_hhd/labeled_ship_2th/5/img'
    # dest_dir = '/home/zoucg/new_hhd/exist_object/5'
    #
    # data = DataProcess(source_dir, dest_dir)
    # data.choose_withobject('txt')

    labeled_data = LabeledDataManager(source_dir, dest_dir)
    labeled_data.selected_error(list_file)


if __name__ == '__main__':
    main()

