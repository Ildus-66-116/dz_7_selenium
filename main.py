from moduls import write_to_csv
from moduls import selenium_hh

if __name__ == '__main__':
    query = input('Введите запрос на hh.ru в форме "Вакансия, Населенный пункт": ')
    data = selenium_hh(query)
    name_file = input('Введите имя файла английской раскладкой: ')
    file_path = name_file + '.csv'
    write_to_csv(file_path, data)
