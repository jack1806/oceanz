import pandas as pd
import re
from datetime import datetime
from bs4 import BeautifulSoup
import os

SHEET_ID = "1drGryXumpzIxMpbdMluybvBMYFK2XSpLadfX_5Re9m0"
SHEET_ENTRY_START_INDEX = 8

COMPUTERS = {
    "CT-ROOM-2": "ct2",
    "CT-ROOM-3": "ct3",
    "CT-ROOM-4": "ct4",
    "CT-ROOM-5": "ct5",
    "CT-ROOM-6": "ct6",
    "CT-ROOM-7": "ct7",
    "T-ROOM-1": "t1",
    "T-ROOM-2": "t2",
    "T-ROOM-3": "t3",
    "T-ROOM-4": "t4",
    "T-ROOM-5": "t5",
    "T-ROOM-6": "t6",
    "T-ROOM-7": "t7",
    "XBOX ONE X": "xbox",
}
LINE_SEPARATOR = "-" * 50
PARA_SEPARATOR = "=" * 50
COLOR_END = '\033[0m'
COLOR_RED = '\033[91m'
COLOR_RED_HIGHLIGHT = '\033[41m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_BLUE = '\033[94m'
BULLET_POINT = '\u2022'


class OceanzEntries:

    def __init__(self, google_sheet_id):
        self.google_sheet = f'https://docs.google.com/spreadsheets/d/{google_sheet_id}/export?format=csv&gid=0'
        self.html_report = f'C:\\Program Files (x86)\\Pan Group\\PanCafe Pro Server\\Report' \
                           f'\\{datetime.today().strftime("%y")}\\' \
                           f'{datetime.today().strftime("%B")}\\' \
                           f'{int(datetime.today().strftime("%d"))}.html'
        self.google_sheet_entries = {}
        self.report_entries = {}
        self.set_sheet_entry()
        self.set_report_entry()

    def set_sheet_entry(self):
        self.google_sheet_entries = {}
        today_int = int(datetime.today().strftime('%d'))
        try:
            df = pd.read_csv(self.google_sheet, header=None)
            today_sheet_entries = [df.iloc[SHEET_ENTRY_START_INDEX+today_int][i]
                                   for i in range(1, len(df.iloc[SHEET_ENTRY_START_INDEX+today_int]))]
            for entry in today_sheet_entries:
                if isinstance(entry, float):
                    break
                entry = entry.split()
                if str(entry[0]).endswith('s') or str(entry[0]).endswith('so'):
                    entry[1] = 'food'
                if entry[1] not in self.google_sheet_entries:
                    self.google_sheet_entries[entry[1]] = 0
                self.google_sheet_entries[entry[1]] += int(re.findall(r'\d+', entry[0])[0])
        except Exception:
            print(f"{COLOR_RED} Failed to load Google Sheet {COLOR_END}")

    def set_report_entry(self):
        self.report_entries = {}
        try:
            html = BeautifulSoup(open(self.html_report, 'rb'), 'lxml')
            amounts = [tag.text for tag in html.find_all('td', attrs={'class': 's6', 'colspan': '10'})]
            members = [tag.text for tag in html.find_all('td', attrs={'class': 's4', 'colspan': '8'})]
            for index in range(len(amounts)):
                amount = amounts[index]
                session = members[index]
                if "(" in members[index] and ")" in members[index]:
                    session = members[index][members[index].find("(") + 1:members[index].find(")")]
                    if session in COMPUTERS:
                        session = COMPUTERS[session]
                if session not in self.report_entries:
                    self.report_entries[session] = 0
                self.report_entries[session] += int(re.findall(r'\d+', amount)[0])
        except Exception:
            print(f"{COLOR_RED} Failed to load HTML report {COLOR_END}")

    @staticmethod
    def compare_entries(sheet_entries, report_entries):
        flag = 0
        print(f"{COLOR_BLUE}Comparing Google Sheet entries with PanCafe{COLOR_END}")
        for google_entry in sheet_entries:
            if google_entry not in report_entries:
                print(f"{BULLET_POINT} {COLOR_YELLOW}Google Sheet entry "
                      f"{COLOR_RED}{google_entry}{COLOR_YELLOW} not found in PanCafe{COLOR_END}")
                flag += 1
            elif sheet_entries[google_entry] != report_entries[google_entry]:
                print(f"{BULLET_POINT} {COLOR_YELLOW}Google Sheet entry --> {COLOR_RED}{google_entry} : "
                      f"{sheet_entries[google_entry]}{COLOR_YELLOW} --- "
                      f"{COLOR_RED}{google_entry} : {report_entries[google_entry]}{COLOR_YELLOW} "
                      f"<-- PanCafe entry{COLOR_END}")
                flag += 1
        if flag == 0:
            print(f"{COLOR_GREEN}No mismatch entry found.{COLOR_END}")
        print(f"{COLOR_BLUE}Comparing PanCafe entries with Google{COLOR_END}")
        flag = 0
        for cafe_entry in report_entries:
            if cafe_entry not in sheet_entries:
                print(f"{BULLET_POINT} {COLOR_YELLOW}PanCafe entry {COLOR_RED}{cafe_entry}{COLOR_YELLOW} "
                      f"not found in Google Sheet{COLOR_END}")
                flag += 1
        if flag == 0:
            print(f"{COLOR_GREEN}No mismatch entry found.{COLOR_END}")


if __name__ == "__main__":
    os.system('color')
    oceanz = OceanzEntries(google_sheet_id=SHEET_ID)
    oceanz.compare_entries(oceanz.google_sheet_entries, oceanz.report_entries)
    input("Press any key to exit...")
