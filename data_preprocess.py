import shutil
import os

class DATA(object):
    def __init__(self, source_dir, dest_dir):
        if os.path.exists(dest_dir) is False:
            os.makedirs(dest_dir)

        self.source_dir = source_dir
        self.dest_dir = dest_dir

    def get_all_flies(self, file_format):
        file_dir = self.source_dir
        files = os.listdir(file_dir)
        files = [fi for fi in files if fi.endswith(file_format)]
        return files

    def choose_withobject(self, files , dest_dir):

        for fi in files:
            fi_path = os.path.join(self.source_dir, fi)
            with open(fi_path, 'rb') as fi_p:
                if len(fi_p.readlines())> 0:
                    dest_sub_dir = os.path.join(self.dest_dir, dest_dir)
                    if os.path.exists(dest_sub_dir) is False:
                        os.makedirs(dest_sub_dir)

                    dest_path = os.path.join(dest_sub_dir, fi)
                    print(dest_path)
                    source_path = os.path.join(self.source_dir, fi)
                    print(source_path)
                    shutil.copy(source_path, dest_sub_dir)
                    shutil.copy(source_path[:-3] + 'png', dest_sub_dir)

def split_end(x):
    return x.split('/')[-1]

def allocate_file(soure_dir, dest_dir=None, num_sub_dir=None):

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







def main():
    # ship = DATA('/media/zoucg/TOSHIBA EXT/labeled_ship/part6', '/home/zoucg/new_hhd/LABELED_SHIP')
    # ship = DATA('/home/zoucg/new_hhd/LABELED_SHIP/slected/part0', '/home/zoucg/new_hhd/LABELED_SHIP/slected/ALL')
    # all_files = ship.get_all_flies('txt')
    # ship.choose_withobject(all_files, 'all')
    allocate_file('/home/zoucg/new_hhd/sub_images_out1', dest_dir='/home/zoucg/new_hhd/out', num_sub_dir=9)


if __name__ == '__main__':
    main()

