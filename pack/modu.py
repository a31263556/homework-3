import csv
import json
import sqlite3

data = [
    ['username', 'password'],
    ['john', 'password123'],
    ['jane', 'qwerty'],
    ['mike', 'letmein'],
    ['sarah', 'abc123'],
    ['wei', '654321']
]

filename = 'users.csv'

with open(filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(data)

print(f'CSV 檔案 {filename} 建立完成！\n')

def read_users_file(filename):
    """
    讀取使用者檔案並返回使用者列表
    """
    users = []
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append(row)
    return users

def read_books_file(filename):
    """
    讀取圖書檔案並返回圖書列表
    """
    with open(filename, 'r', encoding='utf-8') as file:
        books = json.load(file)
    return books

def create_database(db_file):
    """
    建立資料庫和相應的資料表
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 建立使用者表
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    )''')

    # 建立圖書表
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        publisher TEXT NOT NULL,
                        year INTEGER NOT NULL
                    )''')

    conn.commit()
    conn.close()

def insert_users(users, db_file):
    """
    將使用者數據插入使用者表
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    for user in users:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (user['username'], user['password']))

    conn.commit()
    conn.close()

def insert_books(books, db_file):
    """
    將圖書數據插入圖書表
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    for book in books:
        cursor.execute("INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)",
                       (book['title'], book['author'], book['publisher'], book['year']))

    conn.commit()
    conn.close()
