import traceback

from Printer import *
from export import File
from export.DatabaseGlobal import *

path_statements = File.file_path + "statements/"
selected_folder = ""
path_databases = File.file_path.replace("files", "databases")

selected_database = ""
errors = 0

update_pairs = []

# Global iterative constants
company_key = None
statement_key = None
statement_type = None
statement = {}


def insert():
    global company_key, errors

    database_empty = check_database_is_empty()

    for file_num, json in enumerate(File.list_files(path_statements + selected_folder), start=1):
        data = File.read(path_statements + selected_folder + json)

        print("\nAdding company details for: \"" +
              colored(YELLOW, data["name"]) + " (" + colored(YELLOW, data["symbol"]) + ")\"...")

        if database_empty:
            company_key = add_company_details(data)
        else:
            company_key = update_company_details(data)

        try:
            insert_statements(data["statements"])
            print(colored(GREEN, "SUCCESS", True) + " (" + colored(YELLOW, data["symbol"]) + ")")
        except Exception as e:
            tb = str(''.join(traceback.format_exception(None, e, e.__traceback__)))
            File.log_error(data["symbol"], company_key, tb)

            print(error("Err: Something went wrong; added to error log"))
            print(colored(RED, "FAILED", True) + " (" + colored(YELLOW, data["symbol"]) + ")")

            errors += 1

        print(process_notice(file_num))

    print("Database insertion " + colored(GREEN, "COMPLETE", True))


def insert_statements(obj):
    global company_key, statement_key, statement_type, statement, row_number, data_item

    statement_types = list(obj.keys())

    for type in statement_types:
        statement_type = type
        print("Adding " + colored(BLUE, statement_type) + "...")

        connection = establish_connection(selected_database)

        row_number = 1
        statement = obj[statement_type]

        dates = [date for date in statement["Dates"][CELLS]]
        fl_data_items = [data_item for data_item in statement]
        db_data_items = get_data_items_from_database(connection)

        for index, data_item in enumerate(ordered_data_items(db_data_items, fl_data_items)):
            # Data item present in file and in database; update
            if data_item in fl_data_items and data_item in db_data_items:
                statement_key = get_statement_key(connection, data_item)
                update_statement(connection, row_number, data_item, statement[data_item][STYLE])
                update = True
            # Data item present in file but not in database; insert into database
            elif data_item in fl_data_items and data_item not in db_data_items:
                add_statement(connection, row_number, data_item)
                statement_key = get_statement_key(connection, data_item)
                update = False
            # Data item not present in file but present in database; only row number should be updated (no cell tables)
            else:
                update_statement(connection, row_number, data_item)
                row_number += 1
                continue

            insert_data(connection, data_item, dates, update)

            row_number += 1

        connection.close()


def add_company_details(company):
    database = establish_connection(selected_database)

    database.execute("INSERT INTO companies (country, exchange, industry, name, symbol, sector) " +
                     "VALUES (\"" +
                     company["country"] + "\", \"" +
                     company["exchange"] + "\", \"" +
                     company["industry"] + "\", \"" +
                     company["name"] + "\", \"" +
                     company["symbol"] + "\", \"" +
                     company["sector"] + "\");")
    database.commit()

    cursor = database.execute("SELECT CID FROM companies " +
                              "WHERE symbol = \"" + company["symbol"] + "\" " +
                              "AND name = \"" + company["name"] + "\";")

    company_key = get_result(cursor)

    database.close()
    return company_key


def update_company_details(company):
    database = establish_connection(selected_database)

    company_id = get_company_id(company["symbol"])

    database.execute("UPDATE companies SET " +
                     "country = \"" + company["country"] + "\", " +
                     "exchange = \"" + company["exchange"] + "\", " +
                     "industry = \"" + company["industry"] + "\", " +
                     "name = \"" + company["name"] + "\", " +
                     "sector = \"" + company["sector"] + "\" " +
                     "WHERE CID = " + str(company_id) + ";")
    database.commit()
    database.close()

    return company_id


def add_statement(database, row, item):
    global statement_type, company_key, statement

    database.execute("INSERT INTO " + db_rows[statement_type] + " (key, data_item, row_number,style) " +
                     "VALUES (" +
                     str(company_key) + ", \"" +
                     item + "\", " +
                     str(row) + ", '" +
                     statement[item][STYLE] + "');")
    database.commit()


def update_statement(database, row, item, style=None):
    global statement_type, company_key

    update_string = "row_number = " + str(row)
    if style is None:
        update_string += " "
    else:
        update_string += ", style = '" + style + "' "

    database.execute("UPDATE " + db_rows[statement_type] + " SET " +
                     update_string +
                     "WHERE key = " + str(company_key) + " " +
                     "AND data_item = \"" + item + "\";")
    database.commit()


def insert_data(database, item, dates, update):
    global statement, statement_key, statement_type

    db_dates = get_dates_for_data_item(database)

    for index, amount in enumerate(statement[item][CELLS]):
        formatted_date = reformat_date(dates[index])


        if amount == "":
            amount = "NULL"

        insert_string = "INSERT INTO " + db_cells[statement_type] + "(key, period_end, information) " + \
                        "VALUES (" + \
                        str(statement_key) + ", \"" + \
                        formatted_date + "\", " + \
                        amount + ");"

        update_string = "UPDATE " + db_cells[statement_type] + " SET " + \
                        "information = " + amount + " " + \
                        "WHERE key = " + str(statement_key) + " " + \
                        "AND period_end = \"" + formatted_date + "\";"

        if update:
            # If it's an update for a new period, do an insert instead
            if dates[index] not in db_dates:
                database.execute(insert_string)
            # Else update, but only of amount is NULL
            elif amount != "NULL":
                database.execute(update_string)
        # Normal insertion
        else:
            database.execute(insert_string)

        database.commit()


def get_dates_for_data_item(database):
    global statement_type, statement_key

    cursor = database.execute("SELECT period_end FROM " + db_cells[statement_type] + " " +
                              "WHERE key = " + str(statement_key) + ";")

    return [date[0] for date in cursor]


def get_company_id(symbol):
    for pair in update_pairs:
        if symbol == pair[1]:
            return pair[0]
    return 0


def get_data_items_from_database(database):
    global company_key, statement_type

    cursor = database.execute("SELECT data_item FROM " + db_rows[statement_type] + " " +
                              "WHERE key = " + str(company_key) + " " +
                              "ORDER BY row_number ASC;")

    return [data_item[0] for data_item in cursor]


def get_statement_key(database, item):
    global statement_type, company_key

    # Index is used to pair data in "<statement> Cell" table
    cursor = database.execute("SELECT SRID FROM " + db_rows[statement_type] + " " +
                              "WHERE key = " + str(company_key) + " " +
                              "AND data_item = \"" + item + "\";")
    return get_result(cursor)


def check_database_is_empty():
    index_symbol_pair = []
    database = establish_connection(selected_database)

    cursor = database.execute("SELECT * FROM companies")

    for result in cursor:
        index_symbol_pair.append([result[0], result[1]])

    global update_pairs
    update_pairs = index_symbol_pair

    if len(update_pairs) > 0:
        return False
    return True


def ordered_data_items(db_data_items, fl_data_items):
    result = []

    for index, item in enumerate(fl_data_items):
        if index > 0:
            result.append(item)
            if item in db_data_items:
                # Check of next item in database exists in file
                try:
                    next_item_in_db = db_data_items[db_data_items.index(item)+1]
                    # If so, continue
                    if next_item_in_db in fl_data_items:
                        continue
                    # If not, add the database item
                    else:
                        result.append(next_item_in_db)
                # Exception occurs at last item (if it is in the database)
                except:
                    continue

    return result


def get_result(cursor):
    result = None
    for item in cursor:
        result = item[0]
    return result


def reformat_date(date_string):
    # Reformat date from MM/DD/YYYY to YYYY/MM/DD
    if '/' in date_string:
        try:
            month, day, year = date_string.split('/')
            reformatted = year + "/" + month + "/" + day
            return reformatted
        except:
            error("Err: Something went wrong while trying to reformat the date: \"" + date_string + "\"")

    return date_string



def flip_date(date_string):
    # Split the date string into day, month, and year
    day, month, year = date_string.split('/')
    # Concatenate the year, month, and day strings in reverse order
    flipped_date = year + '/' + month + '/' + day
    return flipped_date


def process_notice(file_num, eof=False):
    processed = colored(CYAN, str(file_num)) + " of " + \
                colored(CYAN, str(len(File.list_files(path_statements + selected_folder)))) + " files processed"

    if errors > 0:
        processed += " (" + colored(RED, str(errors)) + ") errors"
    else:
        processed += colored(GREEN, " without ", True) + "any errors"

    if eof:
        return processed
    return processed + "\n"


def clear_database():
    db = establish_connection(selected_database)

    tables = [COMPANIES,
              INCOME_STATEMENT_ROWS,
              BALANCE_SHEET_ROWS,
              CASH_FLOW_ROWS,
              INCOME_STATEMENT_CELLS,
              BALANCE_SHEET_CELLS,
              CASH_FLOW_CELLS]

    for table in tables:
        cursor = db. execute("DELETE FROM " + table + ";")
        print(colored(CYAN, str(cursor.rowcount)) + " rows cleared from \"" + colored(BLUE, table) + "\"...")

    db.commit()
    db.close()
