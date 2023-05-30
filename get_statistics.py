import os
import json
from operator import attrgetter
from collections import namedtuple

EPS = 1E-6

PATH = "statistics/"


def read_data(file) -> dict:
    with open(file, 'r', encoding="utf-8") as file_input:
        data = json.load(file_input)

    return data


def read_all_data() -> dict:
    data = dict()

    all_folders = [file for file in os.listdir(PATH) if os.path.isdir(PATH + file)]

    for folder in all_folders:
        files = [file for file in os.listdir('/'.join([PATH, folder]))]

        for file in files:
            temp_data = read_data('/'.join([PATH, folder, file]))

            for key, value in temp_data.items():
                if data.get(key, None) is None:
                    data[key] = value
                else:
                    for key1, value1 in value["prizes"].items():
                        if data[key]["prizes"].get(key1, None) is None:
                            data[key]["prizes"][key1] = value1
                        else:
                            data[key]["prizes"][key1]["count"] += value1["count"]

    return data


def calculation_case(case) -> tuple:
    case_price = int(case["case_price"])

    frequent_prize = None
    frequent_prize_price = 0
    max_count = 0
    profitably = 0
    unprofitable = 0
    zero = 0
    all_count = 0
    
    for key in case["prizes"].keys():
        price = int(float(case["prizes"][key]["rubles"]))
        count = case["prizes"][key]["count"]
        name = key

        if (price > case_price): profitably += count
        elif (price == case_price): zero += count
        else: unprofitable += count

        if (count > max_count):
            max_count = count
            frequent_prize = name
            frequent_prize_price = price
        elif (count == max_count):
            frequent_prize = name
        
        all_count += count

    percent_non_expression = ((profitably + zero) / all_count) * 100

    return (all_count, profitably, unprofitable, zero, percent_non_expression, frequent_prize, frequent_prize_price, max_count)

def true_title(title) -> str:
    new_title = ""

    for letter in title:
        if (letter.isalnum() or letter == ' '):
            new_title += letter

    return new_title

def get_color(min_percent, max_percent, cur_percent) -> str:
    if abs(cur_percent - 100) < EPS:
        color = f"\033[38;2;{139};{0};{255}m"

    else:
        cur_percent = max(min_percent, min(cur_percent, max_percent))

        middle = abs(max_percent - min_percent) // 2
        red = int(255 * (max_percent - cur_percent) / middle)
        green = int(255 * (cur_percent - min_percent) / middle)

        blue = 0

        color = f"\033[38;2;{red};{green};{blue}m"

    return color


def get_processed_data(data):
    processed_data = list()
    ProcessedTuple = namedtuple('Twists', 'case_name percent_non_expression all_count \
                                profitably unprofitable zero \
                                frequent_prize frequent_prize_price max_count'
    )

    for key in data.keys():
        all_count, profitably, unprofitable, zero, percent_non_expression, frequent_prize, frequent_prize_price, max_count = calculation_case(data[key])
        case_name = data[key]["case_name"]

        '''if (int(percent_non_expression) == 100):
            continue'''

        case_name = true_title(case_name)
        frequent_prize = true_title(frequent_prize)

        processed_data.append(ProcessedTuple(case_name, percent_non_expression, all_count,
                                            profitably, unprofitable, zero,
                                            frequent_prize, frequent_prize_price, max_count
            )
        )

    return processed_data


def write_statistics(data):
    all_count = 0
    normal_color = "\033[0m"
    data.sort(key=lambda x: abs(x.percent_non_expression - 100) < EPS, reverse=True)
    #sorted(data, key=attrgetter('percent_non_expression'))

    print('┏', '━'*53, '┳', '━'*10, '┳', '━'*8, '┳', '━'*8, '┳', '━'*8,
            '┳', '━'*8, '┳', '━'*37, '┳', '━'*6, '┳', '━'*8, '┓', sep=''
    )

    print(
            "┃", '\033[1m', "{:^50s}".format("Название кейса"), 
            "┃", "{:^8s}".format("% побед"),
            "┃", "{:^6s}".format("Кол-во"),
            "┃", "{:^6s}".format("> цены"),
            "┃", "{:^6s}".format("< цены"),
            "┃", "{:^6s}".format("= цене"),
            "┃", "{:^35s}".format("Популярный выигрыш"),
            "┃", "{:^4s}".format("Цена"),
            "┃", "{:^6s}".format("Кол-во"), "┃",
        '\033[0m')

    for note in data:
        '''if (int(percent_non_expression) == 100):
            continue'''

        color = get_color(20, 50, note.percent_non_expression)

        print('┣', '━'*53, '╋', '━'*10, '╋', '━'*8, '╋', '━'*8, '╋', '━'*8,
            '╋', '━'*8, '╋', '━'*37, '╋', '━'*6, '╋', '━'*8, '┫', sep=''
        )

        print(
            "┃", "{:^51s}".format(note.case_name), 
            "┃", "{}{:^7.2f}%{}".format(color, note.percent_non_expression, normal_color),
            "┃", "{:^6d}".format(note.all_count),
            "┃", "{:^6d}".format(note.profitably),
            "┃", "{:^6d}".format(note.unprofitable),
            "┃", "{:^6d}".format(note.zero),
            "┃", "{:^35s}".format(note.frequent_prize),
            "┃", "{:^3d}₽".format(note.frequent_prize_price),
            "┃", "{:^6d}".format(note.max_count), "┃"
        )
        
        all_count += note.all_count

    # print('┗', '━'*53, '┻', '━'*10, '┻', '━'*8, '┻', '━'*8, '┻', '━'*8,
    #         '┻', '━'*8, '┻', '━'*37, '┻', '━'*6, '┻', '━'*8, '┛', sep=''
    # )
    print('┣', '━'*53, '┻', '━'*10, '┻', '━'*8, '┻', '━'*3, '┳', '━'*4, '┻', '━'*8,
        '┻', '━'*8, '┻', '━'*37, '┻', '━'*6, '┻', '━'*8, '┫', sep=''
    )

    print(
        "┃", "{:^75s}".format("Всего обработанных записей"),
        "┃", "{:^74d}".format(all_count), "┃"
    )

    print('┗', '━'*77, '┻', '━'*76, '┛', sep='')
    
    #153 символа не включая левую и правую границу


if __name__ == "__main__":
    data = read_all_data()
    processed_data = get_processed_data(data)
    write_statistics(processed_data)

#return [file for file in os.listdir(path) if os.path.isdir(path + file)]