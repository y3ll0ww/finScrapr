import datetime
import json
import os
import traceback

from Printer import *

file_path = "export/files/"
file_list = {}


def list_files(path):
    return os.listdir(path)


def read(path):
    path_parts = path.split("/")
    print("Reading file " + colored(BLUE, path_parts[len(path_parts)-1]) + "...")
    print("Full path: " + colored(CYAN, path))

    try:
        with open(path, 'r') as file:
            data = json.load(file)
            print("File parsed " + colored(GREEN, "successfully", True))
            file.close()
            return data
    except:
        print(error("\nErr: Not a valid file; make sure it is a json file."))
        return None


def write(dictionary, filename="default", path=None):
    p = file_path

    if path:
        p += path + "/"
        if not os.path.exists(p):
            os.mkdir(p)

    json_object = json.dumps(dictionary, indent=4)

    with open(p + str(datetime.datetime.now().date()) + '_' + filename + ".json", "w") as outfile:
        outfile.write(json_object)

    print("File " + colored(GREEN, "saved", True) + " in: " + colored(CYAN, str(outfile.name)))


def log_error(symbol, company_id, exception):
    p = file_path + "errorlog/"

    entry = str(datetime.datetime.now().strftime("%X")) + ": " + symbol + \
        " (ID:" + str(company_id) + ") " + exception + "\n"

    with open(p + str(datetime.datetime.now().date()) + "_errorlog.txt", "a") as outfile:
        outfile.write(entry)
