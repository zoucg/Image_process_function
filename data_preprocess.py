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

def main():
    # ship = DATA('/media/zoucg/TOSHIBA EXT/labeled_ship/part6', '/home/zoucg/new_hhd/LABELED_SHIP')
    ship = DATA('/home/zoucg/new_hhd/LABELED_SHIP/slected/part0', '/home/zoucg/new_hhd/LABELED_SHIP/slected/ALL')
    all_files = ship.get_all_flies('txt')
    ship.choose_withobject(all_files, 'all')


if __name__ == '__main__':
    main()

