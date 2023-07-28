import sqlite3

class Database:
    def __init__(self, db_uri):
        self.conn = sqlite3.connect(db_uri)
        self.cursor = self.conn.cursor()

    def get_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [r[0] for r in self.cursor.fetchall()]

    def get_primary_key(self, table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = self.cursor.fetchall()
        for column in columns:
            if column[5]:  # The 6th item in the tuple is 1 if the column is the primary key, 0 otherwise
                return column[1], column[2]  # The 2nd item in the tuple is the column name, the 3rd item is the column type
        return None, None

    def get_records(self, table_name, page, per_page):
        offset = (page - 1) * per_page
        self.cursor.execute(f"SELECT * FROM {table_name} LIMIT ? OFFSET ?;", (per_page, offset))
        col_names = [description[0] for description in self.cursor.description]
        records = [dict(zip(col_names, record)) for record in self.cursor.fetchall()]
        return records

    def get_record(self, table_name, key):
        primary_key, _ = self.get_primary_key(table_name)
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE {primary_key} = ?;", (key,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        col_names = [column[0] for column in self.cursor.description]
        return dict(zip(col_names, row))


    def create_record(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' for _ in data)
        self.cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});", tuple(data.values()))
        self.conn.commit()

    def update_record(self, table_name, key, data):
        primary_key, _ = self.get_primary_key(table_name)
        set_clause = ', '.join(f"{column} = ?" for column in data.keys())
        self.cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = ?;", tuple(data.values()) + (key,))
        self.conn.commit()

    def delete_record(self, table_name, key):
        primary_key, _ = self.get_primary_key(table_name)
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {primary_key} = ?;", (key,))
        self.conn.commit()

    def close(self):
        self.conn.close()
