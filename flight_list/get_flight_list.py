import os
import random

from pyflightdata import FlightData
import json
import time

from Config import BASE_DIR


def get_flight_list_loop():  # сбор парка ак
    k = 0
    with open(os.path.join(BASE_DIR, 'data', 'temple_aircraft_flight.json'), 'r') as file:
        set_flight = set(json.load(file))
    aircraft_list = []
    # делаем запрос перерывами от трёх до пяти секунд перерыв между запросами, им обновляем
    # список рейсов до максимального
    while True:
        fdata = FlightData()
        fdata = fdata.get_flights(f'u6{k}')
        k += 1
        # print(k)
        try:
            for i in fdata:
                aircraft_list.append(i['detail']['flight'])
        except AttributeError:
            print('Ошибка получения списка рейсов, какая, мне не интересно')
            # потом сделаю запись в лог
            time.sleep(random.randint(20, 30))

        # print(aircraft_list)
        set_flight.update(aircraft_list)
        # print(len(set_flight))
        aircraft_list = list(set_flight)
        with open(os.path.join(BASE_DIR, 'data', 'temple_aircraft_flight.json'), 'w') as file:
            json.dump(aircraft_list, file, indent=4, ensure_ascii=False)
        aircraft_list = []
        time.sleep(random.randint(1, 5))
        if k == 9999:
            break


def get_history_flight(flight_number):
    time.sleep(random.randint(2, 3))
    fdata = FlightData()
    fdata = fdata.get_history_by_flight_number(flight_number, page=1, limit=10)
    return list(fdata)
    # with open(os.path.join(BASE_DIR, 'data', 'history_list.json'), 'w') as file:
    #     json.dump(history_list, file, indent=4, ensure_ascii=False)


def get_human_button(history_list):
    # with open(os.path.join(BASE_DIR, 'data', 'history_list.json'), 'r') as file:
    #     history_list = json.load(file)
    airport_list = []
    result = {}
    for i in history_list:
        # print()
        # print(i)
        try:
            ap_one = i['airport']['origin']['code']['iata']
        except Exception as ex:
            print(ex)
            continue
        try:
            ap_two = i['airport']['destination']['code']['iata']
        except Exception as ex:
            print(ex)
            continue
        airport_flight = f"{ap_one} - {ap_two}"
        airport_list.append(airport_flight)
        # print(i['airport']['origin']['code']['iata'])
        # print(i['airport']['destination']['code']['iata'])
    local_airports_set = set(airport_list)
    result['number'] = history_list[0]['identification']['number']['default']
    result['flights'] = list(local_airports_set)
    return result


def save_json(data):
    with open(os.path.join(BASE_DIR, 'data', 'button_list.json'), 'r') as file:
        # set_flight = list(set(json.load(file)))
        json_list = list(json.load(file))
    json_list.append(data)
    with open(os.path.join(BASE_DIR, 'data', 'button_list.json'), 'w') as file:
        json.dump(json_list, file, indent=4, ensure_ascii=False)


def clen_blank_flight():
    with open(os.path.join(BASE_DIR, 'data', 'button_list.json'), 'r') as file:
        json_list = list(json.load(file))
    clen_flight_list = []
    for i in json_list:
        if type(i) == dict:
            clen_flight_list.append(i)
    with open(os.path.join(BASE_DIR, 'data', 'clen_button_list.json'), 'w') as file:
        json.dump(clen_flight_list, file, indent=4, ensure_ascii=False)


def main_loop():
    with open(os.path.join(BASE_DIR, 'data', 'temple_aircraft_flight.json'), 'r') as file:
        # set_flight = list(set(json.load(file)))
        set_flight = json.load(file)
    with open(os.path.join(BASE_DIR, 'data', 'button_list.json'), 'w') as file:
        json.dump([], file, indent=4, ensure_ascii=False)
    # button_list = []
    # print(set_flight)
    for i in set_flight:
        print(f'Обработка рейса {i}')
        local_history_flight = get_history_flight(i)
        # print(local_history_flight)
        print(local_history_flight)
        if not local_history_flight:
            print('Список пуст')
            a = i
            save_json(a)
            continue
        else:
            a = get_human_button(local_history_flight)
            save_json(a)



def main():
    pass
    # clen_blank_flight()
    # main_loop()
    # print(a)
    # button_list.append(get_human_button(local_history_flight))
    # button_list.append(a)

    # get_history_flight()
    # get_human_button()

    # while True:
    #     get_flight_list_loop()
    #     # раз в 6 часов
    #     time.sleep(21600)


if __name__ == '__main__':
    main()
