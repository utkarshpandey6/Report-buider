from classes.report1 import Report as Report1
from classes.report2 import Report as Report2
import os


def generateType1Reports():
    report = Report1('file.xlsx')
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
    print("Reading File...")
    locations = report.get_all_locations(include_national_average=True)
    lines = []

    lines.append((report.generate_introduction() + "\n"))
    print("Introduction Completed")
    print("Generating Report...")
    for location in locations:
        print("For location -> " + location)
        lines.append((report.generate_report_for(location) + "\n"))

    print("Writing report to text document")
    file = open("myfile.txt", "w")
    file.writelines(lines)
    file.close()
    os.system('.\myfile.txt')


def generateType2Reports():
    report = Report2('file2.xlsx')
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

    print("Reading File...")
    locations = report.get_all_locations(include_national_average=True)
    lines = []

    lines.append((report.generate_introduction() + "\n"))
    print("Introduction Completed")
    print("Generating Report...")
    for location in locations:
        print("For location -> " + location)

        if location.lower() == "national average":
            lines.append(
                (report.generate_previous_report_for(location) + "\n"))
            lines.append((report.generate_report_for(location) + "\n"))
            lines.append((report.generate_mean_report_for(location) + "\n"))
        else:
            lines.append((report.generate_report_for(location) + "\n"))
            lines.append((report.generate_mean_report_for(location) + "\n"))

    print("Writing report to text document")
    file = open("myfile_type2.txt", "w")
    file.writelines(lines)
    file.close()
    os.system('.\myfile_type2.txt')


def main():
    # generateType1Reports()
    generateType2Reports()


if __name__ == "__main__":
    main()
