import csv

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

import sqlite3
import os

# 檢查資料庫檔是否存在
def check_database_existence(database_name):
    return os.path.exists(database_name)

# 建立資料庫檔及相關資料表
def create_database(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        publisher TEXT NOT NULL,
                        year INTEGER NOT NULL)''')

    conn.commit()
    conn.close()

# 讀取使用者檔，並插入資料表 users
def insert_users_from_file(conn, filename):
    with open(filename, 'r') as file:
        next(file)  # 跳過標頭行
        for line in file:
            username, password = line.strip().split(',')
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

# 讀取圖書檔，並插入資料表 books
def insert_books_from_file(conn, filename):
    with open(filename, 'r') as file:
        next(file)  # 跳過標頭行
        for line in file:
            title, author, publisher, year = line.strip().split(',')
            conn.execute("INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)", (title, author, publisher, int(year)))
        conn.commit()

# 登入功能，最多嘗試三次
def login(conn):
    attempts = 0
    while attempts < 3:
        username = input("請輸入帳號：")
        password = input("請輸入密碼：")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            print("登入成功！")
            return True
        else:
            print("帳號或密碼錯誤，請重新輸入。")
            attempts += 1
    print("登入失敗！程式結束。")
    return False

# 顯示選單
def show_menu():
    print("1.新增圖書")
    print("2.刪除圖書")
    print("3.修改圖書資訊")
    print("4.查詢圖書")
    print("5.圖書清單")
    print("按下Enter結束程式")

# 主程式
def main():
    database_name = 'library.db'
    users_filename = 'users.csv'
    books_filename = 'books.csv'

    # 檢查資料庫檔是否存在，若不存在則建立資料庫及相關資料表
    if not check_database_existence(database_name):
        create_database(database_name)
        conn = sqlite3.connect(database_name)
        insert_users_from_file(conn, users_filename)
        insert_books_from_file(conn, books_filename)
    else:
        conn = sqlite3.connect(database_name)

    # 登入
    if not login(conn):
        conn.close()
        return

    # 顯示選單
    show_menu()
    while True:
        choice = input("請選擇功能：")
        if choice == "":
            break
        else:
            print("無效的選擇")

    conn.close()

if __name__ == "__main__":
    main()
