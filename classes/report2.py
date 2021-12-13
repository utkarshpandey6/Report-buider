import pandas as pd
import numpy as np
from text import introduction_texts, location_texts, national, best_entries_text_when_better_than_checks, best_entries_text_when_worse_than_checks, best_entries_when_only_one_variety_is_better, mean_entries_start, mean_entries_end, mean_entries_start_for_national_average, national_type2, national_type2_without_location
from utils import numToWords
from numpy.core.numeric import NaN
import random
import datetime


class Report():
    def __init__(self, path, sheet="Sheet1"):
        self.file = pd.read_excel(path, sheet_name=sheet)
        self.path = path
        self.locations = []

        for itr in range(1, len(self.file.columns), 3):
            self.locations.append(self.file.columns[itr])

        self.all_entries = []
        self.test_entries = []
        self.check_entries = []
        for itr in range(1, len(self.file[self.file.columns[0]])):
            entry = self.file[self.file.columns[0]][itr]
            if type(entry) != str or entry.lower() == "analysis":
                break
            entry_len = len(entry)
            if entry[entry_len - 1] == "+":
                self.check_entries.append(entry.replace('+', ''))
                self.all_entries.append(entry.replace('+', ''))
            else:
                self.test_entries.append(entry)
                self.all_entries.append(entry)

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
                               "ns": "Non significant"}

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
        self.years = []
        self.previous_years = []
        self.data = []
        self.previous_year_data = []
        self.previous_year_f_test = []
        self.mean_data = []
        self.data_f_test = []
        self.mean_f_test = []
        self.harvesting_dates = []
        self.sowing_dates = []
        for itr in range(len(self.locations)):
            flag = 0
            temp_arr = []
            self.data_f_test.append(
                self.f_test_options[self.file[self.file.columns[((itr + 1) * 3) - 1]][self.f_test_index].lower()])
            self.mean_f_test.append(
                self.f_test_options[self.file[self.file.columns[((itr + 1) * 3)]][self.f_test_index].lower()])
            self.previous_year_f_test.append(
                self.f_test_options[self.file[self.file.columns[(
                    (itr + 1) * 3) - 2]][self.f_test_index].lower()]
            )
            self.harvesting_dates.append(
                self.file[self.file.columns[((itr + 1) * 3) - 1]][self.harvesting_date_index])
            self.sowing_dates.append(
                self.file[self.file.columns[((itr + 1) * 3) - 1]][self.sowing_date_index])
            for item in self.file[self.file.columns[((itr + 1) * 3) - 1]]:
                if flag == 0:
                    self.years.append(item)
                    flag = 1
                    continue
                if (len(temp_arr) == len(self.all_entries)):
                    break
                temp_arr.append(item)
            self.data.append(temp_arr)
            temp_arr = []
            flag = 0
            for item in self.file[self.file.columns[((itr + 1) * 3)]]:
                if flag == 0:
                    flag = 1
                    continue
                if (len(temp_arr) == len(self.all_entries)):
                    break
                temp_arr.append(item)
            self.mean_data.append(temp_arr)
            temp_arr = []
            flag = 0
            for item in self.file[self.file.columns[((itr + 1) * 3) - 2]]:
                if flag == 0:
                    self.previous_years.append(item)
                    flag = 1
                    continue
                if (len(temp_arr) == len(self.all_entries)):
                    break
                temp_arr.append(item)
            self.previous_year_data.append(temp_arr)

        # print("location", self.locations)
        # print("F Test data", self.data_f_test)
        # print("F Test means", self.mean_f_test)
        # print("Years", self.years)
        # print("Check Entries", self.check_entries)
        # print("Test Entries", self.test_entries)
        # print("All Entries", self.all_entries)
        # print("Data", self.data)
        # print("Mean Data", self.mean_data)
        # print(self.harvesting_dates)
        # print(self.sowing_dates)
        # print(self.previous_year_data)
        # print(self.previous_year_f_test)
        # print(self.previous_years)

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
        if location != 'National average':
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
        year = self.years[self.get_index(location, self.locations)]
        type_1 = random.randint(0, len(location_texts) - 1)
        text = location_texts[type_1]
        if location == 'National average':
            type_1 = random.randint(
                0, len(national_type2_without_location) - 1)
            text = national_type2_without_location[type_1]
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

        text = text.format(location=location, year=year, sowing_date=sowing_date, harvesting_date=harvesting_date, age=age, f_test=f_test, best_check=best_check, best_check_value=self.value_to_sentence(best_check_value), best_entry=best_entry,
                           best_entry_value=self.value_to_sentence(best_entry_value), other_best_entries=self.entries_to_sentence(other_best_entries_list), best_checks=self.entries_to_sentence(best_checks))
        return text

    def generate_mean_report_for(self, location):
        f_test = self.get_mean_ftest(location)

        best_entry_list = self.get_mean_best_entries(
            location, better_than_check=True)
        best_entry_list_length = len(best_entry_list)

        type_1 = random.randint(0, len(mean_entries_start) - 1)
        text = mean_entries_start[type_1]
        if location == 'National average':
            type_1 = random.randint(
                0, len(mean_entries_start_for_national_average) - 1)
            text = mean_entries_start_for_national_average[type_1]
        best_checks, best_check, best_entry, other_best_entries_list, type_2, best_check_value, best_entry_value = (
            "", "", "", "", "", "", "")
        if best_entry_list_length == 0:
            best_checks = self.get_mean_best_checks(location)
            best_check_value, best_check = best_checks[0]
            best_entry_value, best_entry = '', ''
            other_best_entries_list = self.get_mean_best_entries(
                location, include_check=True, number=5)
            other_best_entries_list = other_best_entries_list[1:]
            type_2 = random.randint(
                0, len(best_entries_text_when_worse_than_checks) - 1)
            val_temp = best_entries_text_when_worse_than_checks[type_2]
            val_temp = val_temp[0].lower() + val_temp[1:]
            text += val_temp

        elif best_entry_list_length > 1:
            best_checks = self.get_mean_best_checks(location)
            best_check_value, best_check = best_checks[0]
            best_entry_value, best_entry = best_entry_list[0]
            other_best_entries_list = best_entry_list[1:best_entry_list_length]
            type_2 = random.randint(
                0, len(best_entries_text_when_better_than_checks) - 1)
            val_temp = best_entries_text_when_better_than_checks[type_2]
            val_temp = val_temp[0].lower() + val_temp[1:]
            text += val_temp

        elif best_entry_list_length == 1:
            best_checks = self.get_mean_best_checks(location)
            best_check_value, best_check = best_checks[0]
            best_entry_value, best_entry = best_entry_list[0]
            other_best_entries_list = self.get_mean_best_entries(
                location, include_check=True, number=7)
            other_best_entries_list = other_best_entries_list[2:]
            type_2 = random.randint(
                0, len(best_entries_when_only_one_variety_is_better) - 1)
            val_temp = best_entries_when_only_one_variety_is_better[type_2]
            val_temp = val_temp[0].lower() + val_temp[1:]
            text += val_temp

        type_1 = random.randint(0, len(mean_entries_end) - 1)
        text += mean_entries_end[type_1]

        text = text.format(location=location, f_test=f_test, best_check=best_check, best_check_value=self.value_to_sentence(best_check_value), best_entry=best_entry,
                           best_entry_value=self.value_to_sentence(best_entry_value), other_best_entries=self.entries_to_sentence(other_best_entries_list), best_checks=self.entries_to_sentence(best_checks))
        return text

    def generate_previous_report_for(self, location):
        f_test = self.get_previous_ftest(location)

        best_entry_list = self.get_previous_best_entries(
            location, better_than_check=True)
        best_entry_list_length = len(best_entry_list)

        year = self.previous_years[self.get_index(location, self.locations)]
        type_1 = random.randint(0, len(mean_entries_start) - 1)
        text = mean_entries_start[type_1]
        if location == 'National average':
            type_1 = random.randint(
                0, len(national_type2) - 1)
            text = national_type2[type_1]
        best_checks, best_check, best_entry, other_best_entries_list, type_2, best_check_value, best_entry_value = (
            "", "", "", "", "", "", "")
        if best_entry_list_length == 0:
            best_checks = self.get_previous_best_checks(location)
            best_check_value, best_check = best_checks[0]
            best_entry_value, best_entry = '', ''
            other_best_entries_list = self.get_previous_best_entries(
                location, include_check=True, number=5)
            other_best_entries_list = other_best_entries_list[1:]
            type_2 = random.randint(
                0, len(best_entries_text_when_worse_than_checks) - 1)
            val_temp = best_entries_text_when_worse_than_checks[type_2]

            text += val_temp

        elif best_entry_list_length > 1:
            best_checks = self.get_previous_best_checks(location)
            best_check_value, best_check = best_checks[0]
            best_entry_value, best_entry = best_entry_list[0]
            other_best_entries_list = best_entry_list[1:best_entry_list_length]
            type_2 = random.randint(
                0, len(best_entries_text_when_better_than_checks) - 1)
            val_temp = best_entries_text_when_better_than_checks[type_2]

            text += val_temp

        elif best_entry_list_length == 1:
            best_checks = self.get_previous_best_checks(location)
            best_check_value, best_check = best_checks[0]
            best_entry_value, best_entry = best_entry_list[0]
            other_best_entries_list = self.get_previous_best_entries(
                location, include_check=True, number=7)
            other_best_entries_list = other_best_entries_list[2:]
            type_2 = random.randint(
                0, len(best_entries_when_only_one_variety_is_better) - 1)
            val_temp = best_entries_when_only_one_variety_is_better[type_2]

            text += val_temp

        text = text.format(location=location, f_test=f_test, year=year, best_check=best_check, best_check_value=self.value_to_sentence(best_check_value), best_entry=best_entry,
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
        return self.check_entries

    def isCheck(self, entry):
        if entry not in self.get_all_entries(include_check=True):
            raise Exception("Entry doesn't exist")
        if entry in self.check_entries:
            return True
        return False

    def get_best_checks(self, location, number=4):
        if location not in self.file.columns:
            raise Exception("Location Not Found")
        tups = []

        for itr in range(len(self.all_entries)):
            entry = self.all_entries[itr]
            if self.isCheck(entry):
                reading = self.data[self.get_index(
                    location, self.locations)][itr]
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

        li = self.test_entries
        if include_check:
            li = self.all_entries

        for itr in range(len(li)):
            entry = li[itr]
            ind = li.index(entry)
            reading = self.data[self.get_index(
                location, self.locations)][ind]
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

    def get_ftest(self, location):
        if location not in self.file.columns:
            raise Exception("Location Not Found")
        return self.data_f_test[self.get_index(location, self.locations)]

    def get_previous_best_checks(self, location, number=4):
        if location not in self.file.columns:
            raise Exception("Location Not Found")
        tups = []

        for itr in range(len(self.all_entries)):
            entry = self.all_entries[itr]
            if self.isCheck(entry):
                reading = self.previous_year_data[self.get_index(
                    location, self.locations)][itr]
                tups.append((reading, entry))
        tups.sort(reverse=True)
        number = min(number, len(tups))
        return tups[:number]

    def get_previous_best_entries(self, location, include_check=False, better_than_check=False, number=4):
        if location not in self.file.columns:
            raise Exception("Location Not Found")

        tups = []
        if better_than_check:
            include_check = True

        li = self.test_entries
        if include_check:
            li = self.all_entries

        for itr in range(len(li)):
            entry = li[itr]
            ind = li.index(entry)
            reading = self.previous_year_data[self.get_index(
                location, self.locations)][ind]
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

    def get_previous_ftest(self, location):
        if location not in self.file.columns:
            raise Exception("Location Not Found")
        return self.previous_year_f_test[self.get_index(location, self.locations)]

    def get_mean_best_checks(self, location, number=4):
        if location not in self.file.columns:
            raise Exception("Location Not Found")
        tups = []

        for itr in range(len(self.all_entries)):
            entry = self.all_entries[itr]
            if self.isCheck(entry):
                reading = self.mean_data[self.get_index(
                    location, self.locations)][itr]
                tups.append((reading, entry))
        tups.sort(reverse=True)
        number = min(number, len(tups))
        return tups[:number]

    def get_mean_best_entries(self, location, include_check=False, better_than_check=False, number=4):
        if location not in self.file.columns:
            raise Exception("Location Not Found")

        tups = []
        if better_than_check:
            include_check = True

        li = self.test_entries
        if include_check:
            li = self.all_entries

        for itr in range(len(li)):
            entry = li[itr]
            ind = li.index(entry)
            reading = self.mean_data[self.get_index(
                location, self.locations)][ind]
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

    def get_mean_ftest(self, location):
        if location not in self.file.columns:
            raise Exception("Location Not Found")
        return self.mean_f_test[self.get_index(location, self.locations)]

    def get_all_locations(self, include_national_average=False):
        if include_national_average == False:
            loc = []
            for i in self.locations:
                if i.lower() != 'national average':
                    loc.append(i)
            return loc
        return self.locations

    def get_all_entries(self, include_check=False):
        if include_check:
            return self.all_entries
        else:
            return self.test_entries

    def get_number_of_locations(self, include_national_average=False):
        return len(self.get_all_locations(include_national_average))

    def get_number_of_entries(self, include_check=False):
        return len(self.get_all_entries(include_check))

    def get_date_of_sowing(self, location):
        if location not in self.file.columns:
            raise Exception("Location Not Found")
        return self.sowing_dates[self.get_index(location, self.locations)]

    def get_date_of_harvesting(self, location):
        if location not in self.file.columns:
            raise Exception("Location Not Found")
        return self.harvesting_dates[self.get_index(location, self.locations)]

    def get_index(self, value, list):
        if value not in list:
            return -1
        else:
            return list.index(value)
