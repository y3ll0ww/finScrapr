from export.DatabaseGlobal import *


def create_db(name):
    name_db(name)
    database = establish_connection()

    database.execute("""  CREATE TABLE IF NOT EXISTS companies (
        ID                  INTEGER PRIMARY KEY,
        symbol              VARCHAR(10) NOT NULL,
        name                VARCHAR(45) NOT NULL,
        sector              VARCHAR(30) NOT NULL,
        industry            VARCHAR(30) NOT NULL,
        country             VARCHAR(8) NOT NULL,
        exchange            VARCHAR(8) NOT NULL,
        UNIQUE (symbol)    
        );              """)

    create_statement_table(database, INCOME_STATEMENT_ROWS)
    create_statement_table(database, BALANCE_SHEET_ROWS)
    create_statement_table(database, CASH_FLOW_ROWS)

    create_data_table(database, INCOME_STATEMENT_CELLS, INCOME_STATEMENT_ROWS)
    create_data_table(database, BALANCE_SHEET_CELLS, BALANCE_SHEET_ROWS)
    create_data_table(database, CASH_FLOW_CELLS, CASH_FLOW_ROWS)

    database.commit()
    database.close()


def create_statement_table(db_connection, name):
    db_connection.execute("CREATE TABLE IF NOT EXISTS " + name + " ("
                                                                 """
        ID                  INTEGER PRIMARY KEY,
        key                 INTEGER,
        data_item           TEXT NOT NULL,
        row_number          INTEGER NOT NULL,
        style               VARCHAR(10),
        FOREIGN KEY (key)   REFERENCES companies(ID) ON DELETE SET NULL
        );              
                          """)


def create_data_table(db_connection, name, key_name):
    db_connection.execute("CREATE TABLE IF NOT EXISTS " + name + " ("
                                                                 """
        ID                  INTEGER PRIMARY KEY,
        key                 INTEGER,
        period_end          DATE NOT NULL,
        information         DECIMAL(13,10),
        FOREIGN KEY (key)   REFERENCES """ + key_name + "(ID) ON DELETE SET NULL" +
                          ");")
