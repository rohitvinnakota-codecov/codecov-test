import sqlite3, requests, os, json

class DataTransport:
    def __init__(self, db_path="test.db"):
        self.conn = sqlite3.connect(db_path)
        self.session = requests.Session()
        self.cache = {}

    def fetch_from_api(self, url):
        # Reviewer would say: no error handling if network fails
        resp = self.session.get(url)
        return resp.json()

    def save_to_db(self, key, value):
        # Reviewer would say: unhandled DB write errors
        cur = self.conn.cursor()
        cur.execute("INSERT INTO store (k, v) VALUES (?, ?)", (key, value))
        self.conn.commit()

    def delete_from_db(self, key):
        # Reviewer would say: unhandled errors if row doesn’t exist
        cur = self.conn.cursor()
        cur.execute("DELETE FROM store WHERE k=?", (key,))
        self.conn.commit()

    def write_file(self, path, content):
        # Reviewer would say: no error handling for file permissions / disk full
        with open(path, "w") as f:
            f.write(content)

    def read_file(self, path):
        # Reviewer would say: no error handling if file missing
        with open(path, "r") as f:
            return f.read()

    def put_cache(self, key, value):
        # Reviewer would say: fine, but doesn’t handle memory pressure
        self.cache[key] = value

    def remove_cache(self, key):
        # Reviewer would say: unhandled KeyError
        del self.cache[key]

    def sync(self, url):
        # Reviewer would say: unhandled exceptions in combined ops
        data = self.fetch_from_api(url)
        for k, v in data.items():
            self.save_to_db(k, v)
            self.put_cache(k, v)
