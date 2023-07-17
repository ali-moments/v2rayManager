import sqlite3

class DataBase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        # self.cur = self.conn.cursor()
        self.__create_temp_table_ids()
        self.__create_account_table()
        self.__create_temp_admin_fishs()
        self.__create_all_config_table()
        self.commit()

    def __create_temp_table_ids(self):
        self.conn.execute("CREATE TABLE IF NOT EXISTS ids_states(ID INTEGER PRIMARY KEY AUTOINCREMENT, tel_id INTEGER NOT NULL UNIQUE, last_state REAL NOT NULL, last_free TEXT, free_times INTEGER, connected_to_account INTEGER);")
    
    def __create_account_table(self):
        self.conn.execute("CREATE TABLE IF NOT EXISTS accounts(ID INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT  NOT NULL UNIQUE, password TEXT NOT NULL, is_admin INTEGER NOT NULL, subset_id TEXT, money_balanc REAL NOT NULL, gift_balance INTEGER NOT NULL, account_activity INTEGER NOT NULL);")
    
    def __create_temp_admin_fishs(self):
        self.conn.execute("CREATE TABLE IF NOT EXISTS will_check(ID INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, txt_content TEXT, file_path TEXT);")

    def __create_all_config_table(self):
        self.conn.execute("CREATE TABLE IF NOT EXISTS configs(ID INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER  NOT NULL, email_name TEXT NOT NULL, is_active INTEGER NOT NULL, v2_type CHAR(10) NOT NULL);")

    def execute(self, text):
        temp = self.conn.execute(text)
        self.commit()
        return temp

    def fetch(self):
        temp = self.conn.fetchall()
        return temp

    def commit(self):
        self.conn.commit()
    
    def close(self):
        self.conn.commit()
        self.conn.close()