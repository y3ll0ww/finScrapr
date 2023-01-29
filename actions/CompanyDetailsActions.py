import datetime
import json
import os
import traceback
from time import sleep

from Printer import *
from browser import Browser
from export import File, DatabaseGlobal
from refs.pages import DetailsPage

file_path = File.file_path + "companies/"

file_list = {}

dictionary = {"companies": []}

date = str(datetime.datetime.now().date())

total_companies = 0
processed_companies = 0
company_number = 1
skipped = 0


def collect():
    global total_companies, processed_companies, skipped
    file = None

    if list_files():
        print(colored(CYAN, "Available files: ", True))
        for item in file_list:
            print("#" + str(item) + " " + colored(YELLOW, file_list.get(item)))
        file = select_file()
    else:
        print("No files in " + file_path + ".\nRun action for collecting companies first.")

    if file:
        total_companies = len(file["companies"])
        print("\n" + colored(CYAN, str(total_companies)), "companies found")
        create_file(file["companies"])

    print(divider("-----\n\n") + "Fundamental data collection " + colored(GREEN, "complete\n", True) + process_notice())


def list_files():
    dir_list = os.listdir(file_path)

    counter = 1
    for file in dir_list:
        file_list[counter] = file
        counter += 1

    if counter > 1:
        return True
    return False


def select_file():
    while True:
        file = input(user_input("\nSelect json: ") + "#")

        try:
            f = int(file)
            if f in file_list:
                result = File.read(file_path + file_list.get(f))
                if result:
                    return result
            else:
                print(error("Err: No valid file selected; make sure it is within range of available files."))
        except:
            print(error("Err: Not a valid input; type the number of the file to be selected."))


def create_file(json):
    global company_number, skipped
    print("Starting statement collection...\n")

    for company in json:
        symbol = company["symbol"]
        print(divider("-----"))
        print("Checking \"" + colored(YELLOW, company["name"], True) + " (" + colored(YELLOW, symbol, True) + ")\" (" +
              colored(CYAN, str(company_number)) + " of " + colored(CYAN, str(total_companies)) + ")...")

        Browser.go_to(company["link"] + "#statements")

        # Add exchange to object
        try:
            company["exchange"] = DetailsPage.exchange(company["symbol"]).text.replace("[", "").replace("]", "")
        except:
            print(error("Can't find exchange for '" + symbol + "'"))
            if Browser.get_driver().current_url is not company["link"]:
                print(error("No company page found for '" + symbol + "'"))

        # Remove the hyperlink from company object
        company.pop("link")

        # Extract table
        try:
            if DetailsPage.table().is_displayed():
                print("Statements " + colored(GREEN, "available", True) +
                      " for \"" + colored(YELLOW, symbol, True) + "\"")
                extract_company_financials(company)
        except:
            print(error("No statements found for '" + symbol + "', skip to next company..."))
            skipped += 1
            print(process_notice())

        company_number += 1


def extract_company_financials(company):
    global processed_companies, skipped
    company["statements"] = {}

    for statement in DetailsPage.statements():
        try:
            DetailsPage.statements().get(statement).click()
            sleep(0.5)
            print(colored(YELLOW, company["symbol"], True) + ": Collecting data from \"" +
                  colored(BLUE, statement) + "\"...")
        except:
            print(error("Statement not available: \"" + statement + "\""))
            continue

        keys = ["Dates"]
        values = []
        styles = []

        row = 1
        rowsAvailable = True
        while rowsAvailable:
            row_data = []
            style_submitted = False

            try:
                cell = 1
                cellsAvailable = True
                if DetailsPage.td(row, cell).is_displayed():
                    while cellsAvailable:
                        try:
                            content = DetailsPage.td(row, cell).text.replace(",", "")
                            if cell == 2:
                                cell += 1
                                continue
                            if not forbidden(content):

                                if not style_submitted:
                                    if DetailsPage.tr(row).get_attribute("class") == "table-dark-row":
                                        styles.append("BOLD")
                                    else:
                                        styles.append("PLAIN")
                                style_submitted = True

                                if row == 1:
                                    keys.append(content)
                                else:
                                    row_data.append(content)
                            cell += 1
                        except:
                            cellsAvailable = False
                    row += 1
            except:
                rowsAvailable = False

            if len(row_data) > 0:
                values.append(row_data)

        styles.pop(0)
        company["statements"][statement] = make_object(keys, values, styles)

    File.write(company, company["symbol"], "statements/" + date)
    processed_companies += 1

    print(process_notice())


def make_object(keys, values, styles):
    obj = {}

    k = keys[0]
    ks = []
    for i in range(len(keys)):
        inner_object = {DatabaseGlobal.STYLE: "HEAD"}
        if i > 0:
            ks.append(keys[i])
        inner_object[DatabaseGlobal.CELLS] = ks
        obj[k] = inner_object

    for index, array in enumerate(values):
        v = array[0]
        vs = []
        inner_object = {}
        for i in range(len(array)):
            inner_object[DatabaseGlobal.STYLE] = styles[index]
            if i > 0:
                vs.append(array[i])
        inner_object[DatabaseGlobal.CELLS] = vs
        obj[v] = inner_object

    return obj


def forbidden(content):
    decline = [
        "Period End Date",
        "Period Length",
        " Weeks",
        " Months",
        "FINVIZ"
    ]

    for term in decline:
        if content.__contains__(term):
            return True
    return False


def process_notice():
    notice = colored(CYAN, str(processed_companies)) + "/" + \
        colored(CYAN, str(total_companies)) + " companies processed"

    if skipped > 0:
        notice += " (" + colored(RED, str(skipped)) + " skipped)"
    return notice
