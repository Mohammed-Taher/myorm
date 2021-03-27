import sqlite3


class Database:
    def __init__(self, path):
        self.path = path
        self.connection = None
        self.connected = False
        self.connect()

    def get_path(self):
        return self.path

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.path)
            self.connected = True
        except sqlite3.Error as e:
            print(e)
        return self.connection

    def commit(self):
        self.connection.commit()

    def close(self):
        if self.connected:
            self.connection.close()
        self.connected = False
