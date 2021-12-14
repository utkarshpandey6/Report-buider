import pandas as pd
import numpy as np
from text import introduction_texts, location_texts, national, best_entries_text_when_better_than_checks, best_entries_text_when_worse_than_checks, best_entries_when_only_one_variety_is_better
from utils import numToWords
from numpy.core.numeric import NaN
import random
import datetime


class Report():

    def __init__(self, path, sheet="Sheet1"):
        self.file = pd.read_excel(path, sheet_name=sheet)
        self.path = path
        if len(self.file.columns) < 2 or len(self.file[self.file.columns[0]]) < 2:
            raise Exception(
                "Fatal error, file has not been formatted correctly")
        temp = -1
        for i in range(0, len(self.file[self.file.columns[0]])):
            entry = self.file[self.file.columns[0]][i]
            if type(entry) == str and (entry.lower() == "f test" or entry.lower() == "ftest"):
                temp = i
                break
        if temp == -1:
            raise Exception("F test row not found, fatal error")
        self.f_test_index = temp
        self.f_test_options = {"hs": "Highly significant",
                               "sig.": "Significant",
                               "sig": "Significant",
                               "ns": "No significant"}
        self.sowing_date_index = len(self.file[self.file.columns[0]]) - 2
        self.harvesting_date_index = len(self.file[self.file.columns[0]]) - 1

        text_sowing = self.file[self.file.columns[0]
                                ][self.sowing_date_index].lower()
        text_harvesting = self.file[self.file.columns[0]
                                    ][self.harvesting_date_index].lower()

        if "sowing" not in text_sowing and "sowing" not in text_harvesting:
            raise Exception(
                "Date of sowing not found, it should be the second last row of the table")
        if "harvesting" not in text_sowing and "harvesting" not in text_harvesting:
            raise Exception(
                "Date of harvesting not found, it should be the second last row of the table")
        if "sowing" in text_harvesting and "harvesting" in text_sowing:
            print(
                "Date of sowing and date of harvesting rows has been interchanged, reading accordingly ! ")
            temporary = self.sowing_date_index
            self.sowing_date_index = self.harvesting_date_index
            self.harvesting_date_index = temporary

    def generate_introduction(self):

        entries_number = self.get_number_of_entries()
        check_number = self.get_number_of_entries(
            include_check=True) - entries_number
        checks_list = self.get_check_entries()
        location_number = self.get_number_of_locations()
        location_list = self.get_all_locations()
        type = random.randint(0, len(introduction_texts) - 1)

        text = introduction_texts[type].format(number_of_entries=numToWords(
            entries_number),
            number_of_checks=numToWords(
            check_number),
            check_varieties=self.list_to_sentence(
            checks_list),
            number_of_location=numToWords(
            location_number),
            locations=self.list_to_sentence(location_list))
        return text

    def generate_report_for(self, location):

        f_test = self.get_ftest(location)
        sowing_date = ''
        harvesting_date = ''
        age = ''
        print(location.lower())
        if (location.rstrip().lstrip().lower() != "national average"):
            print(location.lower() != 'national average')
            sowing_date = self.get_date_of_sowing(location)
            harvesting_date = self.get_date_of_harvesting(location)
            sowing_date = sowing_date.strftime("%d.%m.%Y")
            harvesting_date = harvesting_date.strftime("%d.%m.%Y")
            age = datetime.datetime.strptime(harvesting_date, "%d.%m.%Y") - \
                datetime.datetime.strptime(sowing_date, "%d.%m.%Y")
            age = str(age.days) + " days"

        # age, _ = (harvesting_date - sowing_date)
        # print(age)
        # if age < 0:
        #     raise Exception(
        #         "Harvesting date cannot be before sowing date for " + location)
        # age = (str(age) + "days")

        best_entry_list = self.get_best_entries(
            location, better_than_check=True)
        best_entry_list_length = len(best_entry_list)

        type_1 = random.randint(0, len(location_texts) - 1)
        text = location_texts[type_1]
        if location.rstrip().lstrip().lower() == "national average":
            type_1 = random.randint(0, len(national) - 1)
            text = national[type_1]
        best_checks, best_check, best_entry, other_best_entries_list, type_2, best_check_value, best_entry_value = (
            "", "", "", "", "", "", "")
        if best_entry_list_length == 0:
            best_checks = self.get_best_checks(location)
            best_check_value, best_check = best_checks[0]
            best_entry_value, best_entry = '', ''
            other_best_entries_list = self.get_best_entries(
                location, include_check=True, number=5)
            other_best_entries_list = other_best_entries_list[1:len(
                other_best_entries_list)]
            type_2 = random.randint(
                0, len(best_entries_text_when_worse_than_checks) - 1)
            text += best_entries_text_when_worse_than_checks[type_2]

        elif best_entry_list_length > 1:
            best_checks = self.get_best_checks(location)
            best_check_value, best_check = best_checks[0]
            best_entry_value, best_entry = best_entry_list[0]
            other_best_entries_list = best_entry_list[1:best_entry_list_length]
            type_2 = random.randint(
                0, len(best_entries_text_when_better_than_checks) - 1)
            text += best_entries_text_when_better_than_checks[type_2]

        elif best_entry_list_length == 1:
            best_checks = self.get_best_checks(location)
            best_check_value, best_check = best_checks[0]
            best_entry_value, best_entry = best_entry_list[0]
            other_best_entries_list = self.get_best_entries(
                location, include_check=True, number=7)
            other_best_entries_list = other_best_entries_list[2:]
            type_2 = random.randint(
                0, len(best_entries_when_only_one_variety_is_better) - 1)
            text += best_entries_when_only_one_variety_is_better[type_2]

        text = text.format(location=location, sowing_date=sowing_date, harvesting_date=harvesting_date, age=age, f_test=f_test, best_check=best_check, best_check_value=self.value_to_sentence(best_check_value), best_entry=best_entry,
                           best_entry_value=self.value_to_sentence(best_entry_value), other_best_entries=self.entries_to_sentence(other_best_entries_list), best_checks=self.entries_to_sentence(best_checks))
        return text

    def entries_to_sentence(self, li):
        text = ""
        length_of_li = len(li)
        for i in range(0, length_of_li):
            li_val, entry = li[i]
            if i == 0:
                text += entry + " " + self.value_to_sentence(li_val)
            elif i == length_of_li - 1 and length_of_li > 1:
                text += " and " + entry + " " + self.value_to_sentence(li_val)
            else:
                text += ", " + entry + " " + self.value_to_sentence(li_val)
        return text

    def value_to_sentence(self, value):
        return "({value} q/ha)".format(value=str(value))

    def list_to_sentence(self, li):
        text = ""
        length_of_li = len(li)
        for i in range(0, length_of_li):
            if i == 0:
                text += li[i]
            elif i == length_of_li - 1 and length_of_li > 1:
                text += " and " + li[i]
            else:
                text += ", " + li[i]
        return text

    def get_check_entries(self):
        entries = []
        for entry in self.file[self.file.columns[0]]:
            if type(entry) != str or entry.lower() == "analysis":
                break
            entry_length = len(entry)
            if entry[entry_length - 1] == '+':
                entry = entry.replace('+', '')
                entries.append(entry)
        return entries

    def get_readings(self, location, include_check=False):
        if location not in self.file.columns:
            raise Exception("Location Not Found")

        entries = self.get_all_entries(include_check=True)
        readings = dict()
        values = self.file[location]
        for i in range(0, len(entries)):
            entry = self.file[self.file.columns[0]][i]
            entry_length = len(entry)
            if entry[entry_length - 1] == '+' and include_check == False:
                continue
            readings[entries[i]] = values[i]
        return readings

    def get_check_reading(self, location):
        if location not in self.file.columns:
            raise Exception("Location Not Found")

        entries = self.get_all_entries(include_check=True)
        readings = dict()
        values = self.file[location]
        for i in range(0, len(entries)):
            entry = self.file[self.file.columns[0]][i]
            entry_length = len(entry)
            if entry[entry_length - 1] == '+':
                readings[entries[i]] = values[i]
        return readings

    def get_date_of_sowing(self, location):
        if location not in self.file.columns:
            raise Exception("Location Not Found")
        return self.file[location][self.sowing_date_index]

    def get_date_of_harvesting(self, location):
        if location not in self.file.columns:
            raise Exception("Location Not Found")
        return self.file[location][self.harvesting_date_index]

    def isCheck(self, entry):
        if entry not in self.get_all_entries(include_check=True):
            raise Exception("Entry doesn't exist")
        if entry in self.get_check_entries():
            return True
        return False

    def get_best_checks(self, location, number=4):
        if location not in self.file.columns:
            raise Exception("Location Not Found")
        tups = []
        readings = self.get_readings(location, include_check=True)
        for entry, reading in readings.items():
            if self.isCheck(entry):
                tups.append((reading, entry))
        tups.sort(reverse=True)
        number = min(number, len(tups))
        return tups[:number]

    def get_best_entries(self, location, include_check=False, better_than_check=False, number=4):
        if location not in self.file.columns:
            raise Exception("Location Not Found")

        tups = []
        if better_than_check:
            include_check = True
        readings = self.get_readings(location, include_check=include_check)
        for entry, reading in readings.items():
            tups.append((reading, entry))
        tups.sort(reverse=True)

        number = min(number, len(tups))
        if better_than_check:
            count = 0
            for _, entry in tups:
                if self.isCheck(entry):
                    break
                count += 1
            number = min(number, count)
        return tups[:number]

    def get_number_of_entries(self, include_check=False):
        count = 0
        for entry in self.file[self.file.columns[0]]:
            if type(entry) != str or entry.lower() == "analysis":
                break
            if entry[len(entry) - 1] == '+' and include_check == False:
                continue
            count += 1
        return count

    def get_number_of_locations(self, include_national_average=False):
        result = len(self.file.columns)
        if include_national_average == False:
            result -= 2
        else:
            result -= 1
        return result

    def get_ftest(self, location):
        value = self.file[location][self.f_test_index]
        if type(value) != str:
            raise Exception(str(value) + " value is not according to type")
        value = value.lower()
        if value not in self.f_test_options:
            raise Exception(str(value) + " is not in options for F test")
        return self.f_test_options[value]

    def get_all_locations(self, include_national_average=False):
        locations = []
        f = 0
        for location in self.file.columns:
            if "national" in location.lower() and "average" in location.lower() and include_national_average == False:
                continue
            if f == 0:
                f = 1
                continue
            locations.append(location)
        return locations

    def get_all_entries(self, include_check=False):
        entries = []
        for entry in self.file[self.file.columns[0]]:
            if type(entry) != str or entry.lower() == "analysis":
                break
            entry_length = len(entry)
            if entry[entry_length - 1] == '+' and include_check == False:
                continue
            if entry[entry_length - 1] == '+':
                entry = entry.replace('+', '')
            entries.append(entry)
        return entries

    def print_all_data(self):
        print(self.file)
