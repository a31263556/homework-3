import sqlite3
import pack.modu as lib

def main():
    # Check if database file exists, if not, create database
    lib.create_database()

    # Insert user data from CSV file
    lib.insert_users_from_csv()

    # Insert book data from JSON file
    lib.insert_books_from_json()

    # Perform login operation
    login_successful = False
    while not login_successful:
        username = input("請輸入帳號：")
        password = input("請輸入密碼：")
        login_successful = authenticate(username, password)
        if not login_successful:
            print("帳號或密碼錯誤，請重新輸入。\n")

    # Display menu
    print_menu()

def authenticate(username, password):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

def print_menu():
    while True:
        print("-------------------")
        print("    資料表 CRUD")
        print("-------------------")
        print("    1. 增加記錄")
        print("    2. 刪除記錄")
        print("    3. 修改記錄")
        print("    4. 查詢記錄")
        print("    5. 資料清單")
        print("-------------------")
        choice = input("選擇要執行的功能(Enter離開)：")
        if choice == "":
            break
        elif choice == "1":
            add_record()
        elif choice == "2":
            delete_record()
        elif choice == "3":
            update_record()
        elif choice == "4":
            search_record()
        elif choice == "5":
            list_records()
        else:
            print("=>無效的選擇\n")

def add_record():
    print("請輸入要新增的標題：")
    title = input()
    print("請輸入要新增的作者：")
    author = input()
    print("請輸入要新增的出版社：")
    publisher = input()
    print("請輸入要新增的年份：")
    year = input()

    if title and author and publisher and year:
        conn = sqlite3.connect("library.db")
        c = conn.cursor()
        c.execute("INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)", (title, author, publisher, year))
        conn.commit()
        conn.close()
        print("異動 1 記錄")
    else:
        print("=>給定的條件不足，無法進行新增作業\n")

def delete_record():
    print("請問要刪除哪一本書？：")
    title = input()
    if title:
        conn = sqlite3.connect("library.db")
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE title=?", (title,))
        conn.commit()
        conn.close()
        print("異動 1 記錄")
    else:
        print("=>給定的條件不足，無法進行刪除作業\n")

def update_record():
    print("請問要修改哪一本書的標題？：")
    title = input()
    if title:
        new_title = input("請輸入要更改的標題：")
        author = input("請輸入要更改的作者：")
        publisher = input("請輸入要更改的出版社：")
        year = input("請輸入要更改的年份：")

        if new_title or author or publisher or year:
            conn = sqlite3.connect("library.db")
            c = conn.cursor()
            c.execute("UPDATE books SET title=?, author=?, publisher=?, year=? WHERE title=?", (new_title, author, publisher, year, title))
            conn.commit()
            conn.close()
            print("異動 1 記錄")
        else:
            print("=>給定的條件不足，無法進行修改作業\n")
    else:
        print("=>給定的條件不足，無法進行修改作業\n")

def search_record():
    keyword = input("請輸入想查詢的關鍵字：")
    if keyword:
        conn = sqlite3.connect("library.db")
        c = conn.cursor()
        c.execute("SELECT title, author, publisher, year FROM books WHERE title LIKE ? OR author LIKE ?", ('%' + keyword + '%', '%' + keyword + '%'))
        rows = c.fetchall()
        conn.close()

        print("|  title  |   author   |  publisher  |   year  |")
        for row in rows:
            print("|" + "  |  ".join(str(item) for item in row) + "  |")
    else:
        print("請輸入有效的關鍵字。\n")

def list_records():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("SELECT title, author, publisher, year FROM books")
    rows = c.fetchall()
    conn.close()

    print("|  title  |   author   |  publisher  |   year  |")
    for row in rows:
        print("|" + "  |  ".join(str(item) for item in row) + "  |")

if __name__ == "__main__":
    main()
