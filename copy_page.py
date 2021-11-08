#!/usr/bin/env python3

# Перед тем как запускать утилиту нужно зайти на сайт под своим логином.
# В режиме разработкика с открытой вкладкой Network обновить страницу. 
# После старта загрузки не дожидаться полной загрузки остановить запись нажав на красный кружок. 
# Выбрать первый загруженный элемент и во вкладке Headers скопировать обновленные user-agent и cookie
# в соответствующее поле ниже в программе.
import requests

# указать начиная с какого дня копировать (число получить можно выбрав на сайте нужную дату и скопировав значение с поля адреса)
user_id = 1589130000000 # - не копируется если нужно чтобы скопироваля закоментируйте первое сложение
DELTA = 86400000
# указываете нужную дату не включая текущую дату так как по ней нет полного списка значений
end_user = 1636218000000
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        'cookie': '_ga=GA1.2.2020144414.1631179045; ruayz=hhs5ih3s3k1umlapn2i3fo2igvna5lkn; _gid=GA1.2.171933959.1636347510; csrf_cookie=3d7d1183da86a621727980b44a800a8a'
    
      }
i = 0
user_id += DELTA  # - если закоментировать это сложение первый будет копироваться
while user_id <= end_user :
    url = 'https://www.ruay.com/member/result/all/%d' % (user_id) # url для второй страницы
    r = requests.get(url, headers = headers)
    with open('dump/%d.html'%(user_id), 'w') as output_file:
        output_file.write(r.text)
    i += 1
    print(user_id)
    user_id += DELTA
    

    
    