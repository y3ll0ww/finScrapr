import traceback

from Printer import *
from export import File
from export.DatabaseGlobal import *

path_statements = File.file_path + "statements/"
path_databases = File.file_path.replace("files", "databases")

selected_database = ""
errors = 0


def insert():
    global errors

    for file_num, json in enumerate(File.list_files(path_statements), start=1):
        data = File.read(path_statements + json)

        print("\nAdding company details for: \"" +
              colored(YELLOW, data["name"]) + " (" + colored(YELLOW, data["symbol"]) + ")\"...")

        company_key = insert_company_details(data)
        try:
            insert_statements(company_key, data["statements"])
            print(colored(GREEN, "SUCCESS", True) + " (" + colored(YELLOW, data["symbol"]) + ")")
        except Exception as e:
            tb = str(''.join(traceback.format_exception(None, e, e.__traceback__)))
            File.log_error(data["symbol"], company_key, tb)

            print(error("Err: Something went wrong; added to error log"))
            print(colored(RED, "FAILED", True) + " (" + colored(YELLOW, data["symbol"]) + ")")

            errors += 1

        print(process_notice(file_num))

    print("Database insertion " + colored(GREEN, "complete", True))
    print(process_notice(len(File.list_files(path_statements)), True))


def insert_company_details(company):
    database = establish_connection(selected_database)

    database.execute("INSERT INTO companies (country, exchange, industry, name, symbol, sector) " +
                     "VALUES (\"" + company["country"] + "\", \"" + company["exchange"] + "\", \"" + company["industry"] +
                     "\", \"" + company["name"] + "\", \"" + company["symbol"] + "\", \"" + company["sector"] + "\");")
    database.commit()

    # There is one exception where the ticker symbol is "ID", causing the select query to fail
    if company["symbol"] != "ID":
        cursor = database.execute("SELECT ID FROM companies " +
                                  "WHERE symbol = \"" + company["symbol"] + "\" AND name = \"" +
                                  company["name"] + "\";")
    else:
        cursor = database.execute("SELECT ID FROM companies " +
                                  "WHERE name = \"" + company["name"] + "\";")

    company_key = get_result(cursor)

    database.close()
    return company_key


def insert_statements(company_key, obj):
    types = list(obj.keys())

    for statement_type in types:
        print("Adding " + colored(BLUE, statement_type) + "...")

        database = establish_connection(selected_database)

        statement = obj[statement_type]
        dates = []
        row_number = 1
        for data_item in statement:
            if data_item == "Dates":
                for date in statement[data_item][CELLS]:
                    dates.append(date)
            else:
                # Key gets added into "<statement> Row" table
                database.execute("INSERT INTO " + db_rows[statement_type] + " (key, data_item, row_number,style) " +
                                 "VALUES (" + str(company_key) + ", \"" + data_item + "\", " +
                                 str(row_number) + ", '" + statement[data_item][STYLE] + "');")
                database.commit()
                # Index is used to pair data in "<statement> Cell" table
                cursor = database.execute("SELECT ID FROM " + db_rows[statement_type] + " "
                                          "WHERE key = " + str(company_key) + " AND data_item = \"" + data_item + "\";")
                statement_key = get_result(cursor)

                # Insert data into "<statement> Cell" table
                # Year is also added in "<statement> Cell" table
                for index, amount in enumerate(statement[data_item][CELLS]):
                    if amount == "":
                        amount = "NULL"

                    database.execute("INSERT INTO " + db_cells[statement_type] + "(key, period_end, information) " +
                                     "VALUES (" + str(statement_key) + ", \"" + dates[index] + "\", " + amount + ");")
                    database.commit()

                row_number += 1

        database.close()


def get_result(cursor):
    result = None
    for item in cursor:
        result = item[0]
    return result


def process_notice(file_num, eof=False):
    processed = colored(CYAN, str(file_num)) + " of " + \
                colored(CYAN, str(len(File.list_files(path_statements)))) + " files processed"

    if errors > 0:
        processed += " (" + colored(RED, str(errors)) + ") errors"
    else:
        processed += colored(GREEN, " without ", True) + "any errors"

    if eof:
        return processed
    return processed + "\n"
