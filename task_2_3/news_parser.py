# -*- coding: utf-8 -*-
import json
import xml
import xml.etree.ElementTree as ET
import chardet
import re

def load_file_contents_xml(file_data):
    file_data_parsed = ET.parse(file_data).getroot()
    print(file_data_parsed)
    for news_description in file_data_parsed.findall('description'):
        print(news_description)
    print('Exit')
    return file_data_parsed


def load_file_contents_json(file_data):
    file_data_parsed = json.loads(file_data)
    cleaned_file_info = ''
    for info in file_data_parsed['rss']['channel']['item']:
        readed_info = str(info['description']['__cdata'])
        cleaned_info = re.sub('<[^<]+?>|; |,|\.|"|/|\n', '', readed_info)
        cleaned_file_info += cleaned_info
    return cleaned_file_info


def load_file(file_name):
    with open(file_name, 'rb') as fhndl:
        file_data = fhndl.read()
    char_result = chardet.detect(file_data)
    str_data = file_data.decode(encoding = char_result['encoding'])
    if file_name[-5:] == '.json':
        res_string = load_file_contents_json(str_data)
    elif file_name[-4:] == '.xml':
        res_string = load_file_contents_xml(file_name)
    else:
        res_string = ''
        print('Не поддерживаемый тип файла')
    return res_string


def statistics_analyze(work_data):
    top10 = {}
    wrk_list = work_data.split(' ')
    word_counter = {}
    for word in wrk_list:
        word_proc = word.strip()
        if len(word_proc) > 6:
            if word_proc in word_counter.keys():
                word_counter[word_proc] += 1
            else:
                word_counter[word_proc] = 1
    sorted_numbers = list(word_counter.values())
    sorted_numbers.sort()
    top10_values = sorted_numbers[-10:]
    for word in word_counter.keys():
        if word_counter[word] in top10_values:
            top10[word] = word_counter[word]
            top10_values.pop()
            if not top10_values:
                break
    return top10


def analyze_news():
    analyzed_files = ['newscy.xml']
    analyzed_files_1 = ['newsafr.json', 'newscy.json', 'newsfr.json', 'newsit.json']
    files_statistics = {}
    for file in analyzed_files:
        ld_data = load_file(file)
        files_statistics[file] = statistics_analyze(ld_data)
    for wfile in files_statistics.keys():
        print('Для файла {}, частотная характеристика: {}'.format(wfile, files_statistics[wfile]))

analyze_news()