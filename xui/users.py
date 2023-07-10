import sqlite3
import os

class User:
    def __init__(self):
        self.connection = sqlite3.connect(os.path.join("xui", "users.db"))
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                chat_id INTEGER PRIMARY KEY,
                username TEXT,
                wallet REAL,
                configs TEXT
            );
        ''')
        self.connection.commit()

    def add_user(self, username: str, chat_id: int) -> None:
        self.cursor.execute(f'''
            INSERT INTO users (chat_id, username, wallet, configs)
            VALUES ({chat_id}, "{username}", 0, "[]");
        ''')
        self.connection.commit()

    def del_user(self, chat_id: int) -> None:
        self.cursor.execute(f'''
            DELETE FROM users
            WHERE chat_id = "{chat_id}";
        ''')
        self.connection.commit()

    def add_config(self, chat_id: int, config: dict) -> None:
        current_configs = self.get_configs(chat_id)
        current_configs.append(config)
        self.cursor.execute(f'''
            UPDATE users
            SET configs = "{str(current_configs)}"
            WHERE chat_id = {chat_id};
        ''')
        self.connection.commit()

    def del_config(self, chat_id: int, config: list) -> None:
        current_configs = self.get_configs(chat_id)
        current_configs.remove(config)
        self.cursor.execute(f'''
            UPDATE users
            SET configs = "{str(current_configs)}"
            WHERE chat_id = {chat_id};
        ''')
        self.connection.commit()

    def add_to_wallet(self, chat_id: int, amount: int) -> None:
        current_wallet = self.get_wallet(chat_id)
        new_wallet = current_wallet + amount
        self.cursor.execute(f'''
            UPDATE users
            SET wallet = {new_wallet}
            WHERE chat_id = {chat_id};
        ''')
        self.connection.commit()

    def remove_from_wallet(self, chat_id: int, amount: int) -> None:
        current_wallet = self.get_wallet(chat_id)
        new_wallet = current_wallet - amount
        self.cursor.execute(f'''
            UPDATE users
            SET wallet = {new_wallet}
            WHERE chat_id = {chat_id};
        ''')
        self.connection.commit()
    
    def set_wallet(self, chat_id: int, amount: int) -> None:
        self.cursor.execute(f'''
            UPDATE users
            SET wallet = {amount}
            WHERE chat_id = {chat_id};
        ''')
        self.connection.commit()
    
    def set_username(self, chat_id: int, username: str) -> None:
        self.cursor.execute(f'''
            UPDATE users
            SET username = "{username}"
            WHERE chat_id = {chat_id};
        ''')
        self.connection.commit()
        
    def get_configs(self, chat_id: int) -> list:
        self.cursor.execute(f'''
            SELECT configs FROM users
            WHERE chat_id = {chat_id};
        ''')
        result = self.cursor.fetchone()
        if result:
            return eval(result[0])
        return []

    def get_wallet(self, chat_id: int) -> int:
        self.cursor.execute(f'''
            SELECT wallet FROM users
            WHERE chat_id = {chat_id}
        ''')
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return 0

    def __del__(self) -> None:
        self.cursor.close()
        self.connection.close()
