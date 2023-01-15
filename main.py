from classes.report1 import Report as Report1
from classes.report2 import Report as Report2
import os
from os.path import isfile, join
from os import listdir


def generateType1Reports():

    # report.print_all_data()
    # print(report.get_all_locations())
    # print(report.get_number_of_entries(include_check=True))
    # print(report.get_all_entries(include_check=True))
    # print(report.get_ftest("Kalyani"))
    # print(report.get_number_of_locations())
    # print(report.get_check_entries())
    # print(report.get_readings("Kalyani", include_check=True))
    # print(report.get_check_reading("Kalyani"))
    # print(report.get_date_of_harvesting("Kalyani"))
    # print(report.get_date_of_sowing("Kalyani"))
    # print(report.get_best_entries("Kalyani", better_than_check=True))
    # print(report.get_best_checks("Kalyani"))
    # print(report.generate_introduction())
    # print(report.generate_report_for("Kalyani"))
    file = open("output_type1.txt", "w")

    files = [f for f in listdir('./input_type1')
             if isfile(join('./input_type1', f))]

    print(files)
    print("\n")
    for rep in files:
        print("Reading " + rep + "...")
        if rep[0] == ".":
            continue
        report = Report1('./input_type1/' + rep)


        locations = report.get_all_locations(include_national_average=True)
        lines = []
        lines.append("Report For File: " + rep + "\n")
        lines.append((report.generate_introduction() + "\n"))
        print("Introduction Completed")
        print("Generating Report...")
        for location in locations:
            print("For location -> " + location)
            lines.append((report.generate_report_for(location) + "\n"))
        lines.append("\n\n")
        print("Writing report to text document")

        file.writelines(lines)
    file.close()


def generateType2Reports():
    file = open("output_type2.txt", "w")
    # report.print_all_data()
    # print(report.get_all_locations())
    # print(report.get_number_of_entries(include_check=True))
    # print(report.get_all_entries(include_check=False))
    # print(report.get_ftest("Kalyani"))
    # print(report.get_number_of_locations())
    # print(report.get_check_entries())

    # print(report.get_date_of_harvesting("Kalyani"))
    # print(report.get_date_of_sowing("Kalyani"))
    # print(report.get_best_entries("Kalyani", better_than_check=True))
    # print(report.get_best_checks("Kalyani"))
    # print(report.generate_introduction())
    # print(report.generate_report_for("Barrackpore"))
    # print(report.generate_mean_report_for("Kalyani"))
    # print(report.generate_previous_report_for("National average"))

    files = [f for f in listdir('./input_type2')
             if isfile(join('./input_type2', f))]

    print(files)
    print("\n")
    for rep in files:
        if rep[0] == ".":
            continue
        report = Report2('./input_type2/' + rep)

        print("Reading " + rep + "....")
        locations = report.get_all_locations(include_national_average=True)
        lines = []
        lines.append("Report For File: " + rep + "\n")
        lines.append((report.generate_introduction() + "\n"))
        print("Introduction Completed")
        print("Generating Report...")
        for location in locations:
            print("For location -> " + location)

            if location.lower() == "national average":
                lines.append(
                    (report.generate_previous_report_for(location) + "\n"))
                lines.append((report.generate_report_for(location) + "\n"))
                lines.append(
                    (report.generate_mean_report_for(location) + "\n"))
            else:
                lines.append((report.generate_report_for(location) + "\n"))
                lines.append(
                    (report.generate_mean_report_for(location) + "\n"))

        lines.append("\n\n")
        print("Writing report to text document")
        file.writelines(lines)
        print("\n\n")

    file.close()


def main():
    print("--------------Generating Report Type 1---------------")
    print("Reading Files")
    generateType1Reports()
    print("--------------Generating Report Type 2---------------")
    print("Reading Files")
    generateType2Reports()

    print("Execution Completed. Press enter.....")
    input()


if __name__ == "__main__":
    main()
