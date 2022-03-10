import os
import json
import webbrowser
import requests
import pyperclip
from time import sleep
from datetime import datetime as date
from tabulate import tabulate


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


appdata = os.getenv('APPDATA')

try:
    key = json.load(open(f"{appdata}\\key.json", "rb"))["key"]
except FileNotFoundError:
    json_data = {"key": " "}
    with open(f"{appdata}\\key.json", "w") as outfile:
        json.dump(json_data, outfile)
    key = json.load(open(f"{appdata}\\key.json", "rb"))["key"]

current_day = date.today().strftime("%A")
api_key = "ApiKeyHere"
api_url = "https://api.jsonbin.io/v3/b/"
api_header = {"X-Master-Key": api_key}


def banner():
    banner = f"""\033[97m
█████████████████████████████████████████
█─▄▄▄─█▄─▄▄─█─▄▄▄▄█─▄─▄─█─▄▄─█─▄▄─█▄─▄███
█─███▀██─▄▄▄█▄▄▄▄─███─███─██─█─██─██─██▀█
▀▄▄▄▄▄▀▄▄▄▀▀▀▄▄▄▄▄▀▀▄▄▄▀▀▄▄▄▄▀▄▄▄▄▀▄▄▄▄▄▀ PlasTec#5267 | V1.0 | {key}
"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)


def mainMenu():
    try:
        banner()
        print("0. EXIT")
        print("1. JOIN MEETING")
        print("2. CREATE TIMETABLE")
        print("3. EDIT KEY")
        print("4. VIEW CURRENT SELECTED TIMETABLE")
        user_input = int(input("> "))
        if -1 < user_input < 5:
            if user_input == 0:
                endMenu()
            if user_input == 1:
                joinmeetingMenu()
            if user_input == 2:
                createtimetableMenu()
            if user_input == 3:
                editkeyMenu()
            if user_input == 4:
                viewtimetable()
        else:
            print(f"{bcolors.FAIL}INVALID CHOICE!{bcolors.ENDC}")
            if input(f"{bcolors.WARNING}WOULD YOU LIKE TO TRY AGAIN? (Y/N): {bcolors.ENDC}").upper() == "Y":
                mainMenu()
            else:
                endMenu()
    except ValueError:
        print(f"{bcolors.FAIL}INVALID INPUT!{bcolors.ENDC}")
        if input(f"{bcolors.WARNING}WOULD YOU LIKE TO TRY AGAIN? (Y/N): {bcolors.ENDC}").upper() == "Y":
            mainMenu()
        else:
            endMenu()


def joinmeetingMenu():
    banner()
    if current_day != "Friday" and current_day != "Saturday":
        if 25 >= len(key):
            r = requests.get(api_url + key, json=None, headers=api_header)
            if r.status_code == 200:
                data = r.json()
                timetable = data["record"]["timetable"][current_day]
                zoomlinks = data["record"]["zoomlinks"]
                for subject in timetable:
                    print(f"{timetable.index(subject) + 1}.{subject}")
                try:
                    subject_choice = int(input("> "))
                    if 0 < subject_choice <= len(timetable):
                        subject_index = subject_choice - 1
                        if len(zoomlinks[timetable[subject_index]]) > 29:
                            webbrowser.open(
                                zoomlinks[timetable[subject_index]])
                            if input(f"{bcolors.WARNING}WOULD YOU LIKE TO GO BACK? (Y/N): {bcolors.ENDC}").upper() == "Y":
                                mainMenu()
                            else:
                                joinmeetingMenu()
                        else:
                            print(f"{bcolors.FAIL}CHECK WHATSAPP!{bcolors.ENDC}")
                            if input(f"{bcolors.WARNING}WOULD YOU LIKE TO GO BACK? (Y/N): {bcolors.ENDC}").upper() == "Y":
                                mainMenu()
                            else:
                                joinmeetingMenu()
                    else:
                        print(f"{bcolors.FAIL}INVALID CHOICE!{bcolors.ENDC}")
                        if input(f"{bcolors.WARNING}WOULD YOU LIKE TO GO BACK? (Y/N): {bcolors.ENDC}").upper() == "Y":
                            mainMenu()
                        else:
                            joinmeetingMenu()
                except ValueError:
                    print(f"{bcolors.FAIL}INVALID INPUT!{bcolors.ENDC}")
                    if input(f"{bcolors.WARNING}WOULD YOU LIKE TO GO BACK? (Y/N): {bcolors.ENDC}").upper() == "Y":
                        mainMenu()
                    else:
                        joinmeetingMenu()
            else:
                print(f"{bcolors.FAIL}INVALID KEY!{bcolors.ENDC}")
                input(f"{bcolors.WARNING}PRESS ENTER TO GO BACK...{bcolors.ENDC}")
                mainMenu()
        else:
            print(f"{bcolors.FAIL}INVALID KEY!{bcolors.ENDC}")
            if input(f"{bcolors.WARNING}WOULD YOU LIKE TO GO BACK? (Y/N): {bcolors.ENDC}").upper() == "Y":
                mainMenu()
            else:
                joinmeetingMenu()
    else:
        print(f"{bcolors.WARNING}THERE IS NO SCHOOL TODAY!{bcolors.ENDC}")
        if input(f"{bcolors.WARNING}WOULD YOU LIKE TO GO BACK? (Y/N): {bcolors.ENDC}").upper() == "Y":
            mainMenu()
        else:
            joinmeetingMenu()


def createtimetableMenu():
    while True:
        data = {"timetable": {"Sunday": [], "Monday": [], "Tuesday": [],
                              "Wednesday": [], "Thursday": []}, "zoomlinks": {}}
        for day in data["timetable"]:
            banner()
            print(f"{day}: ")
            count = 1
            while count <= 8:
                subject = input(f"Period {count}: ").upper()
                if subject:
                    data["timetable"][day].append(subject)
                    count += 1
                else:
                    count = 1
                    break
        banner()
        tabulate_header = ["", "1", "2", "3", "4", "5", "6", "7", "8"]
        tabulate_timetable = [[], [], [], [], []]
        index = 0
        for day in data["timetable"]:
            tabulate_timetable[index].append(day)
            for subject in data["timetable"][day]:
                tabulate_timetable[index].append(subject)
            index += 1
        print(tabulate(tabulate_timetable, headers=tabulate_header))
        if input(f"{bcolors.WARNING}DO YOU LIKE IT? (Y/N): {bcolors.ENDC}").upper() == "Y":
            break
        else:
            if input(f"{bcolors.WARNING}DO YOU WANT TO GO BACK? (Y/N): {bcolors.ENDC}").upper() == "Y":
                mainMenu()

    allsubjects = []
    for day in data["timetable"]:
        allsubjects += data["timetable"][day]
    allsubjects = sorted(list(dict.fromkeys(allsubjects)))

    while True:
        for subject in allsubjects:
            while True:
                banner()
                zoom_code = input(f"{subject}: https://cpsbahrain.zoom.us/j/")
                if len(zoom_code) >= 9 and zoom_code.isdecimal():
                    data["zoomlinks"][subject] = f"https://cpsbahrain.zoom.us/j/{zoom_code}"
                    break
                elif zoom_code == "":
                    data["zoomlinks"][subject] = f"https://cpsbahrain.zoom.us/j/{zoom_code}"
                    break
                else:
                    print(f"{bcolors.WARNING}INVALID CODE!{bcolors.ENDC}")
                    input(f"{bcolors.FAIL}PRESS ENTER TO RETRY{bcolors.ENDC}")

        tabulate_zoomlink = []

        for subject in data["zoomlinks"]:
            tabulate_zoomlink.append([subject, data["zoomlinks"][subject]])

        banner()
        print(tabulate(tabulate_zoomlink))
        if input(f"{bcolors.WARNING}DO YOU LIKE IT? (Y/N): {bcolors.ENDC}").upper() == "Y":
            break
        else:
            if input(f"{bcolors.WARNING}DO YOU WANT TO GO BACK? (Y/N): {bcolors.ENDC}").upper() == "Y":
                mainMenu()

    while True:
        api_header["Content-Type"] = "application/json"
        r = requests.post(api_url, json=data, headers=api_header)
        if r.status_code == 200:
            new_key = r.json()["metadata"]["id"]
            print(f"{bcolors.OKGREEN}Your key is: {new_key}{bcolors.ENDC}")
            pyperclip.copy(new_key)
            api_header.pop("Content-Type")
            input(f"{bcolors.WARNING}PRESS ENTER TO GO BACK...{bcolors.ENDC}")
            break
        else:
            print(f"{bcolors.FAIL}FAILED TO CREATE KEY!{bcolors.ENDC}")
            if input(f"{bcolors.WARNING}WOULD YOU LIKE TO TRY AGAIN? (Y/N): {bcolors.ENDC}").upper() == "N":
                break

    mainMenu()


def editkeyMenu():
    while True:
        banner()
        new_key = input("KEY: ")
        key_json = {"key": new_key}
        if input(f"{bcolors.WARNING}ARE YOU SURE THIS IS THE CORRECT KEY? (Y/N): {bcolors.ENDC}").upper() == "Y":
            break

    with open(f"{appdata}\\key.json", "w") as outfile:
        json.dump(key_json, outfile)
    global key
    key = new_key
    mainMenu()


def viewtimetable():
    banner()
    if 25 >= len(key):
        r = requests.get(api_url + key, json=None, headers=api_header)
        if r.status_code == 200:
            data = r.json()
            timetable = data["record"]["timetable"]
            zoomlinks = data["record"]["zoomlinks"]
            tabulate_header = ["", "1", "2", "3", "4", "5", "6", "7", "8"]
            tabulate_timetable = [[], [], [], [], []]
            index = 0
            for day in timetable:
                tabulate_timetable[index].append(day)
                for subject in timetable[day]:
                    tabulate_timetable[index].append(subject)
                index += 1
            print(tabulate(tabulate_timetable, headers=tabulate_header))

            all_links = []

            for name in zoomlinks:
                all_links.append([name, zoomlinks[name]])

            print(tabulate(all_links))

            input(f"{bcolors.WARNING}PRESS ENTER TO GO BACK...{bcolors.ENDC}")
            mainMenu()
        else:
            print(f"{bcolors.FAIL}INVALID KEY!{bcolors.ENDC}")
            input(f"{bcolors.WARNING}PRESS ENTER TO GO BACK...{bcolors.ENDC}")
            mainMenu()
    else:
        print(f"{bcolors.FAIL}INVALID KEY!{bcolors.ENDC}")
        input(f"{bcolors.WARNING}PRESS ENTER TO GO BACK...{bcolors.ENDC}")
        mainMenu()


def endMenu(timer=3):
    for i in range(timer, 0, -1):
        banner()
        print(
            f"Thanks for using CPSTOOL developed by PlasTec. Exiting in {i} seconds...")
        sleep(1)
    exit()


mainMenu()
