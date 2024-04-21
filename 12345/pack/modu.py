import sqlite3
import csv
import json
import os

def create_database():
    if not os.path.exists("library.db"):
        conn = sqlite3.connect("library.db")
        c = conn.cursor()

        # Create users table
        c.execute('''CREATE TABLE users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                     )''')

        # Create books table
        c.execute('''CREATE TABLE books (
                        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        publisher TEXT NOT NULL,
                        year INTEGER NOT NULL
                     )''')

        conn.commit()
        conn.close()

def insert_users_from_csv():
    with open('users.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            username, password = row
            conn = sqlite3.connect("library.db")
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()

def insert_books_from_json():
    with open('books.json', 'r') as file:
        books = json.load(file)
        conn = sqlite3.connect("library.db")
        c = conn.cursor()
        for book in books:
            title = book['title']
            author = book['author']
            publisher = book['publisher']
            year = book['year']
            c.execute("INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)", (title, author, publisher, year))
        conn.commit()
        conn.close()
