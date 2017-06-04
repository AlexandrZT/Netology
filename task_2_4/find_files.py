import glob
import os.path


migrations = 'Migrations'


def locate_files(folder):
    files = glob.glob(os.path.join(folder, "*.sql"))
    return files


def search_data(search_at_files):
    file_list_iter = search_at_files
    while True:
        search_string = input('Введите строку для поиска(!q - для выхода): ')
        if search_string == '!q':
            break
        file_list = []
        for file in file_list_iter:
            with open(file, 'r') as fsearch:
                if search_string in fsearch.read():
                    file_list.append(file)
                    print(file)
        print('{}'.format(len(file_list)))
        file_list_iter = file_list

look_files = locate_files(migrations)
search_data(look_files)
