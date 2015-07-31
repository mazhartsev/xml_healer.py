#!/usr/bin/python3
# -*- coding: utf-8 -*-

# xml_healer.py v1

'''
Скрипт для исправления невалидных XML файлов. 
Автор: Dmitry Mazhartsev 
e-mail: uksvlg@yandex.ru
Распространяется на условиях лицензии «Attribution-ShareAlike» («Атрибуция — На тех же условиях») 4.0 Всемирная
CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0/deed.ru
'''

import os
import sys
import re

# =====================================================================
out = 'out'             # Папка с обработанными файлами
enc = 'windows-1251'    # Кодировка файлов
ext = '.xml'            # Расширение файла
EXT = '.XML'
end = '</Файл>'         # Закрывающий тег
file_dir = os.getcwd()  # Текущая директория
filler = '='*70         # Заполнитель
# =====================================================================
# Если папка out отсутствует, то создать её
if os.path.exists(out) == False:
    os.mkdir(out)

# =====================================================================
# Список регулярных выражений и замен
regexp = [
['\&(?!lt;|gt;|amp;|quot;|apos;)', '&amp;'],    # Замена символа &
['<(?=[\d\>\<])', '&lt;'],                      # Замена символа <
['(?<=[";])<', '&lt;'],                         # Замена символа <
['<(?=[-])', '&lt;'],                           # Замена символа <
#['(?<=[\&lt;\>\d])>','&gt;'],                   # Замена символа >
['(?<=[\&lt;\>])>','&gt;'],                   # Замена символа >
['→',''],                                       # Замена символа →
['«', '&quot;'],                                # Замена символа «
['»', '&quot;'],                                # Замена символа »
['\"\"', '\"']                                  # Удаление задвоения символов "
]

# =====================================================================
# Лечащая функция

def healer(file, enc):
    out_file = '{0}/{1}'.format(out,file)       # Исцеленный файл
    #print(out_file)
    try:
        # Открыть исходный файл в режиме чтения, конченый в режиме записи
        with open(file, encoding=enc) as sick_file, open(out_file, 'w', encoding=enc) as heal_file:

            # Построчное чтение и запись
            for f in sick_file:
                for r in regexp:
                    f = re.sub(r[0], r[1], f)

                if f.startswith(end):
                    f = end
                    heal_file.write(f)
                    break
                else:
                    heal_file.write(f)
            print('Исцелен!\n')
            
    except UnicodeDecodeError:
            print('Файл имеет кодировку отличную от {}\n'.format(enc))
            error_file_list.append(file)
            os.remove(out_file)

# =====================================================================
print(filler)
print('Текущий каталог: {}'.format(file_dir))
print('Папка с обработанными файлами: {}'.format(os.path.abspath(out)))
print(filler)

# Поиск xml файлов в текущей директории
xml_list = []                       # пустой список для xml
error_file_list = []
file_list = os.listdir(file_dir)    # список всех файлов в папке

for file in file_list:
    print('Имя файла: {}'.format(file))
    if file.endswith(ext):
        xml_list.append(file)
        healer(file, enc)
    elif file.endswith(EXT):
        xml_list.append(file)
        healer(file, enc)    
    else:
        print('Не является XML-файлом\n')

# =====================================================================
# Информация об обработанных файлах
xml_list = list(set(xml_list).difference(error_file_list))

print(filler)
print('Обработаны следующие файлы:')
for i in xml_list:
    print('- {0}'.format(i))

if len(error_file_list) > 0:
    print('\nФайлы с кодировкой отличной от {}:'.format(enc))
    for i in error_file_list:
        print('- {0}'.format(i))

print('\nОбработанные файлы находятся в папке: {}'.format(os.path.abspath(out)))


print('''
О проблемах в работе скрипта сообщайте по адресу uksvlg@yandex.ru
Dmitry Mazhartsev CC BY-SA 4.0''')

# Завершение работы скрипта
input('\nНажмите Enter')
