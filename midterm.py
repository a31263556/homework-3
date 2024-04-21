import sqlite3
import pack.modu as lib

def display_menu():
    """
    顯示操作選單
    """
    print("-------------------")
    print("    資料表 CRUD")
    print("-------------------")
    print("    1. 新增記錄")
    print("    2. 刪除記錄")
    print("    3. 修改記錄")
    print("    4. 查詢記錄")
    print("    5. 資料清單")
    print("-------------------")

def main():
    # 檢查資料庫是否存在
    db_file = "library.db"
    lib.create_database(db_file)

    # 讀取使用者檔案和圖書檔案
    users = lib.read_users_file("users.csv")
    books = lib.read_books_file("books.json")

    # 將使用者數據和圖書數據插入資料庫
    lib.insert_users(users, db_file)
    lib.insert_books(books, db_file)

    # 使用者登入
    authenticated = False
    while not authenticated:
        username = input("請輸入帳號：")
        password = input("請輸入密碼：")

        # 檢查使用者名稱和密碼是否匹配資料庫中的記錄
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            authenticated = True
        else:
            print("帳號或密碼不正確，請重新輸入。")

    # 顯示菜單
    while True:
        display_menu()
        choice = input("選擇要執行的功能(Enter離開)：")

        if choice == "1":
            # 新增圖書記錄
            pass
        elif choice == "2":
            # 刪除圖書記錄
            pass
        elif choice == "3":
            # 修改圖書記錄
            pass
        elif choice == "4":
            # 查詢圖書記錄
            pass
        elif choice == "5":
            # 顯示圖書清單
            pass
        else:
            print("=>無效的選擇")
            continue

if __name__ == "__main__":
    main()
