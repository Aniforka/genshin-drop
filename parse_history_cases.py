import os
import json
import requests
from time import sleep
import datetime

PATH = "statistics"

BANNED_CASES = [
    # "24-chasa-oskolki",
    # "besplatnye-60-kristallov",
    # "do-1090-kristallov-za-druzey",
    # "keys-za-podpisku-telegramm",
    # "do-330-kristallov-za-popolnenie",
    # "pooshhrenie-do-2240-kristallov-za-popolnenie-ot-200r",
    # "gd_system_case"
]

def get_cases() -> dict:
    data = dict()

    with open("cases.json", 'r', encoding="utf-8") as file_input:
        data = json.load(file_input)

    return data

def check_history(cases) -> list:
    history_url = "https://genshindrop.com/api/live"

    data = list()

    response = requests.get(history_url).json()["data"]

    for loot in response:
        prize_rubles = loot["amount"]
        prize_name = loot["item"]["name"]
        case_name = loot["box"]["name"]
        case_short_url = loot["box"]["slug"]
        case_price = cases[case_short_url]
        key = loot["key"]
    
        if (case_short_url not in BANNED_CASES):
            data.append(
                {
                    "case_short_url":case_short_url,
                    "case_name":case_name,
                    "case_price": case_price,
                    "prize_rubles":prize_rubles,
                    "prize_name":prize_name,
                    "key":key
                }
            )

    return data

def save_row_data(data) -> None:
    with open("RowData.txt", 'a+', encoding="utf-8") as file_output:
        for record in data:
            file_output.write(
                "{}:{}:{}:{}:{}\n".format(
                    record["case_short_url"], record["case_name"], record["prize_rubles"], record["prize_name"], record["key"]
                )
            )

def processing_data(data, current_file, previous_file) -> None:
    old_data = read_data(current_file)
    
    for record in data:
        prize_rubles = record["prize_rubles"]
        prize_name = record["prize_name"]
        case_name = record["case_name"]
        case_short_url = record["case_short_url"]
        prize_key = record["key"]
        case_price = record["case_price"]

        if (old_data.get(case_short_url) == None):
            old_data[case_short_url] = {
                "case_name":case_name,
                "case_price":case_price,
                "prizes":{},
                "keys":[]
            }
        
        if (old_data[case_short_url]["prizes"].get(prize_name) == None):
            old_data[case_short_url]["prizes"][prize_name] = {
                "rubles":prize_rubles,
                "count":0
            }
        

        old_file_keys = list()

        if os.path.isfile(previous_file):
            temp_data = read_data(previous_file)
            old_file_keys = temp_data[case_short_url]["keys"]
        

        if ((prize_key not in old_data[case_short_url]["keys"]) and (prize_key not in old_file_keys)):
            old_data[case_short_url]["prizes"][prize_name]["count"] += 1
            old_data[case_short_url]["keys"].append(prize_key)

    write_data(old_data, current_file)


def create_file_path(date) -> str:
    folder_name = date.strftime('%d-%m-%Y')
    file_name = date.strftime('%H')

    return "{0}/{1}/{2}.json".format(PATH, folder_name, file_name)


def read_data(path) -> dict:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = dict()

    if os.path.isfile(path):
        with open(path, 'r', encoding="utf-8") as file_input:
            data = json.load(file_input)

    return data

def write_data(data, path) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w', encoding="utf-8") as file_output:
        json.dump(data, file_output, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    cases = get_cases()

    while True:
        try:
            data = check_history(cases)
            #print(data)
            #save_row_data(data)

            processing_data(
                data,
                create_file_path(datetime.datetime.now()),
                create_file_path(datetime.datetime.now() - datetime.timedelta(hours=1))
            )
            print('a')
        except Exception as exp: print(exp)

        sleep(3)
