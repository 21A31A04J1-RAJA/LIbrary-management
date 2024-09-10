import sqlite3
from datetime import datetime

# Create a connection to the SQLite database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create tables if not already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL,
        is_available INTEGER DEFAULT 1
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        membership_date TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Borrow (
        member_id INTEGER,
        book_id INTEGER,
        borrow_date TEXT,
        return_date TEXT,
        FOREIGN KEY(member_id) REFERENCES Members(id),
        FOREIGN KEY(book_id) REFERENCES Books(id)
    )
''')

conn.commit()

# Log file to store past transactions
log_file = 'transaction_log.txt'

# Function to log transactions to a file
def log_transaction(action, member_id, book_id, date):
    with open(log_file, 'a') as file:
        file.write(f'{action} - Member ID: {member_id}, Book ID: {book_id}, Date: {date}\n')

# Function to add a new book
def add_book(title, author, year):
    cursor.execute('INSERT INTO Books (title, author, year) VALUES (?, ?, ?)', (title, author, year))
    conn.commit()
    print(f'Book "{title}" added successfully!')

# Function to list all books
def list_books():
    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()
    for book in books:
        status = "Available" if book[4] else "Borrowed"
        print(f'ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Year: {book[3]}, Status: {status}')

# Function to add a new member
def add_member(name, membership_date):
    cursor.execute('INSERT INTO Members (name, membership_date) VALUES (?, ?)', (name, membership_date))
    conn.commit()
    print(f'Member "{name}" added successfully!')

# Function to list all members
def list_members():
    cursor.execute('SELECT * FROM Members')
    members = cursor.fetchall()
    for member in members:
        print(f'ID: {member[0]}, Name: {member[1]}, Membership Date: {member[2]}')

# Function to borrow a book
def borrow_book(member_id, book_id, borrow_date):
    cursor.execute('SELECT is_available FROM Books WHERE id = ?', (book_id,))
    is_available = cursor.fetchone()[0]
    
    if is_available:
        cursor.execute('INSERT INTO Borrow (member_id, book_id, borrow_date) VALUES (?, ?, ?)', (member_id, book_id, borrow_date))
        cursor.execute('UPDATE Books SET is_available = 0 WHERE id = ?', (book_id,))
        conn.commit()
        log_transaction('Borrowed', member_id, book_id, borrow_date)
        print(f'Book with ID {book_id} borrowed by Member ID {member_id}.')
    else:
        print(f'Book with ID {book_id} is already borrowed.')

# Function to return a book
def return_book(member_id, book_id, return_date):
    cursor.execute('UPDATE Books SET is_available = 1 WHERE id = ?', (book_id,))
    cursor.execute('UPDATE Borrow SET return_date = ? WHERE member_id = ? AND book_id = ?', (return_date, member_id, book_id))
    conn.commit()
    log_transaction('Returned', member_id, book_id, return_date)
    print(f'Book with ID {book_id} returned by Member ID {member_id}.')

# Function to view transaction history from the log file
def view_past_transactions():
    print("Past Transactions:")
    try:
        with open(log_file, 'r') as file:
            logs = file.readlines()
            for log in logs:
                print(log.strip())
    except FileNotFoundError:
        print("No transaction records found.")

# Menu for interacting with the system
def menu():
    while True:
        print('''
        Library Management System
        1. Add Book
        2. List Books
        3. Add Member
        4. List Members
        5. Borrow Book
        6. Return Book
        7. View Past Transactions
        8. Exit
        ''')
        choice = input('Enter your choice: ')
         
        if choice == '1':
            title = input('Enter book title: ')
            author = input('Enter book author: ')
            year = int(input('Enter book publication year: '))
            add_book(title, author, year)
        
        elif choice == '2':
            list_books()
        
        elif choice == '3':
            name = input('Enter member name: ')
            membership_date = input('Enter membership date (YYYY-MM-DD): ')
            add_member(name, membership_date)
        
        elif choice == '4':
            list_members()
        
        elif choice == '5':
            while True:
                member_id = input('Enter member ID (10 characters): ')
                if len(member_id) == 10:
                    # print("Valid member ID!")
                    break
                else:
                    print("Invalid member ID! Please enter exactly 6 characters.")
            # member_id = input('Enter member ID: ')
            book_id = int(input('Enter book ID: '))
            borrow_date = input('Enter borrow date (YYYY-MM-DD): ')
            borrow_book(member_id, book_id, borrow_date)
        
        elif choice == '6':
            while True:
                member_id = input('Enter member ID (10 characters): ')
                if len(member_id) == 10:
                    # print("Valid member ID!")
                    break
                else:
                    print("Invalid member ID! Please enter exactly 6 characters.")           
            book_id = int(input('Enter book ID: '))
            return_date = input('Enter return date (YYYY-MM-DD): ')
            return_book(member_id, book_id, return_date)
        
        elif choice == '7':
            view_past_transactions()
        
        elif choice == '8':
            print("Exiting...")
            conn.close()
            break
        
            
        
        else:
            print('Invalid choice! Please try again.')

# Start the menu
menu()
