#!/usr/bin/env python3
# проверка всех вариантов наборов на выигрышность сколько как часто и есть ли
# прибыль по итогу играут 2 числа из 3 правое число
# не все игры берем если убрать коментарий

import requests
from bs4 import BeautifulSoup
from lxml import html
import time
import json

dir_name = 'dump'
data_file_name = "db.json"
first_file_name = 1579194000000
last_file_name = 1636218000000

delta = 86400000

file_name = first_file_name
data_base = []

#############################################################
def parce_datafile_lxml(file_name):
    result = []
    with open("%s/%d.html"%(dir_name, file_name), "r") as fr:
        r = fr.read()
    soap = BeautifulSoup(r, 'lxml')
    div_pills = soap.find('div', {'id': 'pills-tabContent'})
    div_pc = div_pills.find_all('div', {'class': ['carousel-item active', 'carousel-item']})
    i =0
    for div in div_pc:
        numbers = div.find_all('p', {'class': 'card-text'})
        j = 0
        for number in numbers:
            num = 0
            if number.text == 'xxx' or number.text == 'xx':
                num = -1
            else: num = int(number.text)
            if j == 0 :
                result.append([num,0])
                j += 1
            else :
                result[i][1] = num
                j=0
        i += 1
    return result
#===================================== body ======================

#загружаем данные для анализа из файлов предварительно загруженных с сайта
while file_name <= last_file_name :
    date_of_file = time.ctime(file_name // 1000)
    print(date_of_file)
    data_base.append([date_of_file,parce_datafile_lxml(file_name)])
    file_name += delta

with open("%s/%s"%(dir_name, data_file_name), "a") as write_file:
    json.dump(data_base, write_file)
