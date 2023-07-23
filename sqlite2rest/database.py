import sqlite3

class Database:
    def __init__(self, db_uri):
        self.conn = sqlite3.connect(db_uri, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [r[0] for r in self.cursor.fetchall()]

    def get_primary_key(self, table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = self.cursor.fetchall()
        for column in columns:
            if column[5]:  # The 6th item in the tuple is 1 if the column is the primary key, 0 otherwise
                return column[1]  # The 2nd item in the tuple is the column name
        return None

    def get_records(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name};")
        return self.cursor.fetchall()

    def get_record(self, table_name, key):
        primary_key = self.get_primary_key(table_name)
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE {primary_key} = ?;", (key,))
        return self.cursor.fetchone()

    def create_record(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' for _ in data)
        self.cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});", tuple(data.values()))
        self.conn.commit()

    def update_record(self, table_name, key, data):
        primary_key = self.get_primary_key(table_name)
        set_clause = ', '.join(f"{column} = ?" for column in data.keys())
        self.cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = ?;", tuple(data.values()) + (key,))
        self.conn.commit()

    def delete_record(self, table_name, key):
        primary_key = self.get_primary_key(table_name)
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {primary_key} = ?;", (key,))
        self.conn.commit()

