import requests
import urllib

def translate_it(text, file_name=None, save_file=None, from_language=None, to_languge='ru'):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'

    params = {
        'key': key,
        'lang': 'ru-en',
        'text': text,
    }
    response = requests.get(url, params=params).json()
    return ' '.join(response.get('text', []))


def show_avaliable_languages():
    url = 'https://translate.yandex.net/api/v1.5/tr.json/getLangs'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
    params = {
        'key': key,
        'ui': 'ru',
    }
    response = requests.get(url, params=params).json()
    for lang in response['langs'].keys():
        print('Язык: {}, код {}.'.format(response['langs'][lang], lang))
    print(' '.join(response.get('text', [])))


def detect_language(text):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
    params = {
        'key': key,
        'text': urllib.parse.quote_plus(text),
    }
    response = requests.get(url, params=params).json()
    return 'Предпологаемый язык: {}'.format(response['lang'])



#print(detect_language("Rompiendo con una tradiciГіn diplomГЎtica con "))
#show_avaliable_languages()
#a = translate_it('Привет')
