import requests
import urllib
import os


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
    Function translate_it allows translate text with Yandex translator.
    Function accepts following paraments:
    text          - Text to translate
    file_name     - File to translate < 10kb
    save_file     - File to save translation results
    from_language - Language from which traslation should be done
    to_languge    - Language to which traslation should be done
    If function recieve text or file wihtout save file it would return translated text.
    If function recieve save_file it will return 0 in success case.
    text parametr has precendance over file_name
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
    to_translate = ''
    if file_name:
        file_stat =  os.stat(file_name)
        if file_stat.st_size / 1024 > 10:
           print('Слишком большой файл.')
           return
        else:
            with open(file_name, 'r') as rfile:
                to_translate = rfile.read()
    if text:
        if len(text) > 10000:
            print('Слишком длинный текст.')
            return
        else:
            to_translate = text
    params = {
        'key': key,
        #'text': urllib.parse.quote_plus(to_translate),
        'text': to_translate,
        'options': 1,
    }
    if from_language:
        params['lang'] = '{}-{}'.format(from_language, to_languge)
    else:
        params['lang'] = to_languge
    response = requests.post(url, params=params).json()
    translation = urllib.parse.unquote(response['text'][0])
    if save_file:
        with open(save_file, 'w') as wfile:
            wfile.write(translation)
        return
    else:
        return translation


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
    if response.status == 200:
        return response['lang']
    else:
        return -1


#print('Предпологаемый язык: {}'.format(detect_language("Rompiendo con una tradiciГіn diplomГЎtica con "))
#show_avaliable_languages()
transl = translate_it('',file_name='DE.txt')
if transl:
    print(transl)
