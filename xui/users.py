import sqlite3
import os

class Users:
    def __init__(self):
        self.db_path = os.path.join("xui", "users.db")
        self.create_table()

    def create_table(self) -> None:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                chat_id INTEGER PRIMARY KEY,
                username TEXT,
                wallet REAL,
                configs TEXT
            );
        ''')
        connection.commit()
        cursor.close()
        connection.close()

    def add_user(self, username: str, chat_id: int) -> None:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(f'SELECT username FROM users WHERE chat_id = "{chat_id}";')
        result = cursor.fetchone()
        if not result:
            cursor.execute(f'''
                INSERT INTO users (chat_id, username, wallet, configs)
                VALUES ({chat_id}, "{username}", 0, "[]");
            ''')
            connection.commit()
        cursor.close()
        connection.close()

    def del_user(self, chat_id: int) -> None:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(f'''
            DELETE FROM users
            WHERE chat_id = "{chat_id}";
        ''')
        connection.commit()
        cursor.close()
        connection.close()

    def add_config(self, chat_id: int, config: dict) -> None:
        current_configs = self.get_configs(chat_id)
        current_configs.append(config)
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(f'''
            UPDATE users
            SET configs = "{str(current_configs)}"
            WHERE chat_id = {chat_id};
        ''')
        connection.commit()
        cursor.close()
        connection.close()

    def del_config(self, chat_id: int, config: list) -> None:
        current_configs = self.get_configs(chat_id)
        current_configs.remove(config)
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(f'''
            UPDATE users
            SET configs = "{str(current_configs)}"
            WHERE chat_id = {chat_id};
        ''')
        connection.commit()
        cursor.close()
        connection.close()

    def add_to_wallet(self, chat_id: int, amount: int) -> None:
        current_wallet = self.get_wallet(chat_id)
        new_wallet = current_wallet + amount
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(f'''
            UPDATE users
            SET wallet = {new_wallet}
            WHERE chat_id = {chat_id};
        ''')
        connection.commit()
        cursor.close()
        connection.close()

    def remove_from_wallet(self, chat_id: int, amount: int) -> None:
        current_wallet = self.get_wallet(chat_id)
        new_wallet = current_wallet - amount
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(f'''
            UPDATE users
            SET wallet = {new_wallet}
            WHERE chat_id = {chat_id};
        ''')
        connection.commit()
        cursor.close()
        connection.close()
    
    def set_wallet(self, chat_id: int, amount: int) -> None:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(f'''
            UPDATE users
            SET wallet = {amount}
            WHERE chat_id = {chat_id};
        ''')
        connection.commit()
        cursor.close()
        connection.close()
    
    def set_username(self, chat_id: int, username: str) -> None:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(f'''
            UPDATE users
            SET username = "{username}"
            WHERE chat_id = {chat_id};
        ''')
        connection.commit()
        cursor.close()
        connection.close()

    def get_configs(self, chat_id: int) -> list:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(f'''
            SELECT configs FROM users
            WHERE chat_id = {chat_id};
        ''')
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return eval(result[0])
        return []

    def get_wallet(self, chat_id: int) -> int:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(f'''
            SELECT wallet FROM users
            WHERE chat_id = {chat_id}
        ''')
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return result[0]
        return 0
