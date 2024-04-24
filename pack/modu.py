import sqlite3
import csv
import json

DATABASE_FILE = 'library.db'
USERS_FILE = 'users.csv'
BOOKS_FILE = 'books.json'

# 選單提示訊息
MENU_PROMPT = '''-------------------
    資料表 CRUD
-------------------
    1. 增加記錄
    2. 刪除記錄
    3. 修改記錄
    4. 查詢記錄
    5. 資料清單
-------------------
選擇要執行的功能(Enter離開)：'''

# 無效選擇訊息
INVALID_CHOICE_MSG = '=>無效的選擇'

def setup_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # 建立 users 資料表
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    )''')

    # 建立 books 資料表
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        publisher TEXT NOT NULL,
                        year INTEGER NOT NULL
                    )''')

    # 讀取使用者檔並插入資料庫
    with open(USERS_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (row['username'], row['password'])
            )

    # 讀取圖書檔並插入資料庫
    with open(BOOKS_FILE, 'r', encoding='utf-8') as jsonfile:
        books_data = json.load(jsonfile)
        for book in books_data:
            cursor.execute(
                "INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)",
                (book['title'], book['author'], book['publisher'], book['year'])
            )

    conn.commit()
    conn.close()

def login():
    while True:
        username = input("請輸入帳號：")
        password = input("請輸入密碼：")

        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # 檢查帳號密碼是否正確
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return user
        else:
            print("帳號或密碼錯誤，請重新輸入")

def execute_menu_choice(choice):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    if choice == 1:
        add_record(cursor)
    elif choice == 2:
        delete_record(cursor)
    elif choice == 3:
        modify_record(cursor)
    elif choice == 4:
        search_record(cursor)
    elif choice == 5:
        list_records(cursor)

    conn.commit()
    conn.close()

def add_record(cursor):
    title = input("請輸入要新增的標題：")
    author = input("請輸入要新增的作者：")
    publisher = input("請輸入要新增的出版社：")
    year = input("請輸入要新增的年份：")

    if title and author and publisher and year:
        cursor.execute("INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)",
                       (title, author, publisher, year))
        print("異動 1 記錄")
    else:
        print("=>給定的條件不足，無法進行新增作業")

def delete_record(cursor):
    title = input("請問要刪除哪一本書？：")
    if title:
        cursor.execute("DELETE FROM books WHERE title = ?", (title,))
        print("異動 1 記錄")
    else:
        print("=>給定的條件不足，無法進行刪除作業")

def modify_record(cursor):
    title = input("請問要修改哪一本書的標題？：")
    new_title = input("請輸入要更改的標題：")
    new_author = input("請輸入要更改的作者：")
    new_publisher = input("請輸入要更改的出版社：")
    new_year = input("請輸入要更改的年份：")

    if title:
        cursor.execute("UPDATE books SET title = ?, author = ?, publisher = ?, year = ? WHERE title = ?",
                       (new_title, new_author, new_publisher, new_year, title))
        print("異動 1 記錄")
    else:
        print("=>給定的條件不足，無法進行修改作業")

def search_record(cursor):
    keyword = input("請輸入想查詢的關鍵字：")
    if keyword:
        cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR publisher LIKE ? OR year LIKE ?",
                       (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        print_records(cursor.fetchall())
    else:
        print("關鍵字不能為空")

def list_records(cursor):
    cursor.execute("SELECT * FROM books")
    print_records(cursor.fetchall())

def print_records(records):
    if not records:
        print("沒有符合條件的記錄")
    else:
        print("|　　　　書名　　　　|　　　　作者　　　　|　　　出版|年份　　　")  # Add a closing quotation mark at the end of the string
