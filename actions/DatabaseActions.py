from Printer import *
from export import DatabaseCreation, DatabaseInsertion, File
from export.DatabaseGlobal import db_path


def create():
    while True:
        try:
            database_name = input(user_input("Name of new database: "))
            DatabaseCreation.create_db(database_name)
            print("Database \"" + colored(YELLOW, database_name, True) + "\" created")
            print("Find it in folder \"" + colored(CYAN, db_path) + "\"")
            break
        except:
            print(error("Err: Something went wrong, please try again"))
            continue


def clear():
    select_db()

    print(error("WARNING: selected database \"") + colored(YELLOW, DatabaseInsertion.selected_database) +
          error("\" will be whiped of all data. Do you wish to proceed?"))

    while True:
        choice = input(user_input("Y/N: "))

        if choice.upper() not in ["Y", "N"]:
            print(error("Type either \"Y\" or \"N\" (not case sensitive)"))
        elif choice.upper() == "Y":

            DatabaseInsertion.clear_database()

            print("Clearing of database \"" +
                  colored(YELLOW, DatabaseInsertion.selected_database) + "\" " + colored(GREEN, "successful"))

            break
        elif choice.upper() == "N":
            print("Clearing of database \"" +
                  colored(YELLOW, DatabaseInsertion.selected_database) + "\" " + colored(RED, "aborted"))

            break
        else:
            print(error("Err: Something went wrong, please try again later"))


def insert():
    select_db()
    select_dir()

    num_files = len(File.list_files(DatabaseInsertion.path_statements + DatabaseInsertion.selected_folder))
    print(colored(CYAN, str(num_files)) + " files will be inserted into database \""
          + colored(YELLOW, DatabaseInsertion.selected_database) + "\"...\n")

    DatabaseInsertion.insert()


def select_db():
    available_databases = File.list_files(DatabaseInsertion.path_databases)

    if len(available_databases) < 1:
        print(error("Err: There are no available databases found, please create one first."))
    else:
        print(colored(CYAN, "Select an available database:", True))

        counter = 1
        for database in available_databases:
            print("#" + str(counter) + " " + colored(YELLOW, database))
            counter += 1

        while True:
            num = input(user_input("\nSelect database: ") + "#")
            try:
                DatabaseInsertion.selected_database = available_databases[int(num)-1]
                print("Selected \"" + colored(YELLOW, DatabaseInsertion.selected_database) + "\"...\n")
                break
            except:
                print(error("Err: Invalid input; type a valid number of the database in the list"))


def select_dir():
    print(colored(CYAN, "Select a folder to parse: ", True))

    available_folders = File.list_files(DatabaseInsertion.path_statements)

    counter = 1
    for folder in available_folders:
        nf = len(File.list_files(DatabaseInsertion.path_statements + folder))
        print("#" + str(counter) + " " + colored(YELLOW, folder) + " (" + colored(CYAN, str(nf)) + " files)")
        counter += 1

    while True:
        num = input(user_input("\nSelect folder: ") + "#")
        try:
            DatabaseInsertion.selected_folder = available_folders[int(num)-1] + "/"
            print("\nSelected \"" + colored(YELLOW, DatabaseInsertion.selected_folder.replace("/", "")) + "\"...")
            break
        except:
            print(error("Err: Invalid input; type a valid number of the folder in the list"))
