import os
import subprocess
import glob
import multiprocessing


def convert(binary, image_name, dst_folder):
    dst_file = os.path.join(dst_folder,os.path.basename(image_name))
    subprocess.run([binary, image_name, '-resize', '200', dst_file])

def locate_files(folder):
    return glob.glob(os.path.join(folder,'*.jpg'))


def prepare_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)

def convert_worker(binary, image_name, dst_folder):
    print(binary, image_name, dst_folder)

def convert_images(converter, dst_file):
    thread_count = 0
    while not thread_count in ['s', 'm', '1', '4']:
        thread_count = input('Запустить 1 поток(s) или 4ре(m)?:')
    folder_name = 'Source'
    convert_files = locate_files(folder_name)
    prepare_folder(dst_file)
    if thread_count.lower() in ['s', '1']:
        for img in convert_files:
            convert(converter, convert_files[0], dst_file)
    elif thread_count.lower() in ['m', '4']:
        thread_count = '4'
        wprocess = []
        for pnom in range(int(thread_count)):
            mproc = multiprocessing.Process(target=convert, args=(converter, convert_files[pnom], dst_file))
            wprocess.append(mproc)
            mproc.start()
        for wproc in wprocess:
            wproc.join()



if __name__ ==  '__main__':
    converter_bin = 'convert.exe'
    destination_folder = 'Destination'
    convert_images(converter_bin, destination_folder)
