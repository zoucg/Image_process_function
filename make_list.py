import os

def make_list(dir, file,des_dir=None,dest_file=None):
    trains = []
    with open(dir+file,'rb') as f:
        train_list= f.readlines()
        for t in train_list:
            s = t.split('\\')
            s = s[-1][:-5]+'\r\n'
            trains.append(s)

    if os.path.exists(des_dir) is False:
        os.makedirs(des_dir)

    with open(des_dir+dest_file, 'wb') as f1:
        f1.writelines(trains)









def main():
    make_list('./', 'train_box-300-GF2.txt','./voc/ImageSets/Main/','train.txt')
    make_list('./', 'val_box-300-GF2.txt','./voc/ImageSets/Main/','test.txt')

if __name__== '__main__':
    main()
