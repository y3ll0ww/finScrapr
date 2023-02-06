import sqlite3

db_name = ""
db_path = "export/databases/"

INCOME_STATEMENT_DB = "Income Statement"
BALANCE_SHEET_DB = "Balance Sheet"
CASH_FLOW_DB = "Cash Flow"

COMPANIES = "companies"

INCOME_STATEMENT_ROWS = "income_statement_rows"
BALANCE_SHEET_ROWS = "balance_sheet_rows"
CASH_FLOW_ROWS = "cash_flow_rows"

INCOME_STATEMENT_CELLS = "income_statement_cells"
BALANCE_SHEET_CELLS = "balance_sheet_cells"
CASH_FLOW_CELLS = "cash_flow_cells"

STYLE = "style"
CELLS = "cells"

db_rows = {
    INCOME_STATEMENT_DB: INCOME_STATEMENT_ROWS,
    BALANCE_SHEET_DB: BALANCE_SHEET_ROWS,
    CASH_FLOW_DB: CASH_FLOW_ROWS
}

db_cells = {
    INCOME_STATEMENT_DB: INCOME_STATEMENT_CELLS,
    BALANCE_SHEET_DB: BALANCE_SHEET_CELLS,
    CASH_FLOW_DB: CASH_FLOW_CELLS
}


def name_db(name):
    global db_name
    db_name = name


def establish_connection(name=None):
    if name:
        return sqlite3.connect(db_path + name)
    return sqlite3.connect(db_path + db_name)
