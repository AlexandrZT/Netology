import glob
import os.path

migrations = 'Migrations'

files = glob.glob(os.path.join(migrations, "*.sql"))
print(type(files))
file_list_iter = files
cntr = 10
while True:
    search_string = input('Введите строку для поиска(!q - для выхода): ')
    if search_string == '!q':
        break
    file_list = []
    for file in file_list_iter:
        if search_string in open(file).read():
            file_list.append(file)
            print(file)
    print('{}'.format(len(file_list)))
    file_list_iter = file_list
    cntr -= 1