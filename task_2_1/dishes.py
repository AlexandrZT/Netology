import os

def load_cook_book(file_name):
    loaded_cook_book = {}
    recepie_cntr = 0
    read_file = True
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            while read_file:
                recepie_name = f.readline().lower().strip()
                if recepie_name == '':
                    read_file = False
                    continue
                ingredients_num = int(f.readline())
                loaded_cook_book[recepie_name] = []
                recepie_cntr += 1
                for item in range(ingredients_num):
                    ingredient = f.readline().lower()
                    list_ingedients = ingredient.split('|')
                    loaded_cook_book[recepie_name].append({'ingridient_name': list_ingedients[0].strip(), \
                                                       'quantity': int(list_ingedients[1].strip()), 'measure': list_ingedients[2].strip()})
    else:
        print('Ошибка загрузки файла рецептов.')
        return False
    print('Загружено {} рецепта(ов).'.format(recepie_cntr))
    return loaded_cook_book

def get_shop_list_by_dishes(dishes, person_count, cook_book):
    shop_list = {}
    for dish in dishes:
        for ingridient in cook_book[dish]:
            new_shop_list_item = dict(ingridient)
            new_shop_list_item['quantity'] *= person_count
            if new_shop_list_item['ingridient_name'] not in shop_list:
                shop_list[new_shop_list_item['ingridient_name']] = new_shop_list_item
            else:
                shop_list[new_shop_list_item['ingridient_name']]['quantity'] += new_shop_list_item['quantity']
    return shop_list


def print_shop_list(shop_list):
    for shop_list_item in shop_list.values():
        print('{} {} {}'.format(shop_list_item['ingridient_name'], shop_list_item['quantity'],
                                shop_list_item['measure']))


def create_shop_list():
    cook_book_file = input('Введите имя файла:')
    if cook_book_file:
        wrk_cook_book = load_cook_book(cook_book_file)
    else:
        wrk_cook_book = {}
        print("Не загружен файл рецептов. Выход.")
    person_count = int(input('Введите количество человек: '))
    dishes = input('Введите блюда в расчете на одного человека (через запятую): ') \
        .lower().split(', ')
    shop_list = get_shop_list_by_dishes(dishes, person_count, wrk_cook_book)
    print_shop_list(shop_list)

create_shop_list()
