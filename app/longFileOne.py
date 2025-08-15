import os, sys, re, math, time, random, threading, multiprocessing, asyncio
import sqlite3, json, requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functools import wraps
from argparse import ArgumentParser

DB_FILE = "data.db"

def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} executed in {time.time() - start:.2f}s")
        return result
    return wrapper

class DataProcessor:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, text TEXT, value REAL)''')
        self.conn.commit()

    def insert_entry(self, text, value):
        c = self.conn.cursor()
        c.execute('INSERT INTO entries (text, value) VALUES (?, ?)', (text, value))
        self.conn.commit()

    def query_entries(self):
        c = self.conn.cursor()
        return c.execute('SELECT * FROM entries').fetchall()

    def close(self):
        self.conn.close()

@log_time
def simulate_web_fetch():
    r = requests.get("https://httpbin.org/get")
    return r.json()

def regex_filter(lines, pattern):
    return [line for line in lines if re.search(pattern, line)]

def generate_data(n=1000):
    return pd.DataFrame({
        "x": np.linspace(0, 10, n),
        "y": np.sin(np.linspace(0, 10, n)) + np.random.normal(0, 0.1, n)
    })

@log_time
def plot_data(df):
    plt.plot(df['x'], df['y'])
    plt.title("Noisy Sine Wave")
    plt.savefig("plot.png")
    plt.close()

async def async_fetch(url):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, requests.get, url)

@log_time
def run_async_tasks():
    urls = [f"https://httpbin.org/delay/{i%3}" for i in range(5)]
    results = asyncio.run(asyncio.gather(*[async_fetch(url) for url in urls]))
    return [r.status_code for r in results]

def thread_task(n):
    print(f"Thread {n} sleeping...")
    time.sleep(random.uniform(0.5, 2.0))
    print(f"Thread {n} done.")

def run_threads():
    threads = [threading.Thread(target=thread_task, args=(i,)) for i in range(5)]
    [t.start() for t in threads]
    [t.join() for t in threads]

def process_task(x):
    return math.sqrt(x ** 2 + 1)

def run_processes():
    with multiprocessing.Pool(4) as pool:
        return pool.map(process_task, range(10000))

def write_large_file(filename, n=100000):
    with open(filename, "w") as f:
        for i in range(n):
            f.write(f"{i},value={random.random()}\n")

def read_and_process_file(filename):
    with open(filename) as f:
        return sum(1 for line in f if float(line.split('=')[1]) > 0.5)

def main():
    parser = ArgumentParser()
    parser.add_argument("--file", type=str, default="large.txt")
    parser.add_argument("--insert", action="store_true")
    args = parser.parse_args()

    write_large_file(args.file)
    print("File written.")
    count = read_and_process_file(args.file)
    print(f"Lines with value > 0.5: {count}")

    dp = DataProcessor(DB_FILE)
    if args.insert:
        for _ in range(100):
            dp.insert_entry("sample", random.random())
    entries = dp.query_entries()
    print(f"Loaded {len(entries)} DB entries.")
    dp.close()

    data = generate_data()
    plot_data(data)
    print("Plot saved.")
    run_threads()
    print("Threading done.")
    result = run_processes()
    print(f"Process result sample: {result[:5]}")
    print("Async fetch status codes:", run_async_tasks())
    print("Web fetch sample:", simulate_web_fetch())

if __name__ == "__main__":
    main()
