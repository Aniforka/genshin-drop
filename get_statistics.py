import os
import time
import json

def read_data() -> dict:
    with open("prepared_data.json", 'r', encoding="utf-8") as file_input:
        data = json.load(file_input)

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
    cur_percent = max(min_percent, min(cur_percent, max_percent))

    middle = abs(max_percent - min_percent) // 2
    red = int(255 * (max_percent - cur_percent) / middle)
    green = int(255 * (cur_percent - min_percent) / middle)

    blue = 0

    color = f"\033[38;2;{red};{green};{blue}m"

    return color

def write_statistics(data):
    normal_color = "\033[0m"

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

    for key in data.keys():
        all_count, profitably, unprofitable, zero, percent_non_expression, frequent_prize, frequent_prize_price, max_count = calculation_case(data[key])
        case_name = data[key]["case_name"]

        '''if (int(percent_non_expression) != 100):
            continue'''

        case_name = true_title(case_name)
        frequent_prize = true_title(frequent_prize)
        color = get_color(20, 50, percent_non_expression)

        print('┣', '━'*53, '╋', '━'*10, '╋', '━'*8, '╋', '━'*8, '╋', '━'*8,
            '╋', '━'*8, '╋', '━'*37, '╋', '━'*6, '╋', '━'*8, '┫', sep=''
        )
        print(
            "┃", "{:^51s}".format(case_name), 
            "┃", "{}{:^7.2f}%{}".format(color, percent_non_expression, normal_color),
            "┃", "{:^6d}".format(all_count),
            "┃", "{:^6d}".format(profitably),
            "┃", "{:^6d}".format(unprofitable),
            "┃", "{:^6d}".format(zero),
            "┃", "{:^35s}".format(frequent_prize),
            "┃", "{:^3d}₽".format(frequent_prize_price),
            "┃", "{:^6d}".format(max_count), "┃"
        )

    print('┗', '━'*53, '┻', '━'*10, '┻', '━'*8, '┻', '━'*8, '┻', '━'*8,
            '┻', '━'*8, '┻', '━'*37, '┻', '━'*6, '┻', '━'*8, '┛', sep=''
        )

if __name__ == "__main__":
    SPEED = 300

    while True:
        data = read_data()
        os.system('cls')
        write_statistics(data)
        time.sleep(SPEED)
