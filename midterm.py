import pack.modu as lib

def main():
    # 建立資料庫並讀取資料
    lib.setup_database()
    # 登入驗證
    user = lib.login()
    if user:
        # 顯示選單
        while True:
            choice = input(lib.MENU_PROMPT)
            if not choice:
                break
            elif choice.isdigit():
                choice = int(choice)
                if choice in range(1, 6):
                    lib.execute_menu_choice(choice)
                else:
                    print(lib.INVALID_CHOICE_MSG)
            else:
                print(lib.INVALID_CHOICE_MSG)

if __name__ == "__main__":

    main()
