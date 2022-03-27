import mysql.connector as sqlctr
import sys

mycon = sqlctr.connect(host='localhost', user='root', password='')

if mycon.is_connected():
    print('Successfully connected to localhost')
else:
    print('Error while connecting to localhost')
cursor = mycon.cursor()

# creating database
cursor.execute("drop database if exists dhruv_library")
cursor.execute("create database if not exists dhruv_library")
cursor.execute("use dhruv_library")

# creating the tables we need

cursor.execute('''
    create table
    if not exists books(
        SN int(5) PRIMARY KEY AUTO_INCREMENT,
        Book_Name varchar(30),
        Quantity_Available int(10),
        Price_Per_Day int(10)
    )
''')
cursor.execute('''
    create table
    if not exists BORROWER(
        SN int(5) PRIMARY KEY AUTO_INCREMENT,
        borrowers_name varchar(40),
        book_lent varchar(20),
        contact_no varchar(15)
    )
''')

def command(st):
    cursor.execute(st)

def fetch():
    data = cursor.fetchall()
    for i in data:
        print(i)

def describe(tname):
    st = 'desc '+ tname
    command(st)
    data = cursor.fetchall()
    columns = []
    for i in data:
        columns.append(i[0])
    print(tuple(columns))

def all_data(tname):
    print('\n')
    print('-------List of all '+tname+'-------\n')
    describe(tname)
    st = 'select * from '+tname
    command(st)
    fetch()

def add_book():
    n = int(input('Enter number of books to be added: '))
    values = []
    for _ in range(n):
        name = input('Enter book name: ')
        qty = int(input('Enter the available quantity of book: '))
        while qty <= 0 and qty > 100:
            qty = int(input('Enter the available quantity of book: '))
        price = int(input('Enter per day price of book: '))
        while price <= 0 and price > 2000:
            price = int(input('Enter per day price of book: '))
        values.append((name, qty, price,))
        print()
    cursor.executemany("INSERT INTO books (Book_Name, Quantity_Available, Price_Per_Day) VALUES (%s, %s, %s)", values)
    print("\nDATA INSERTED SUCCESSFULLY\n")

def lend():
    print('\n___AVAILABLE BOOKS___\n')
    st0 = 'select Book_Name from books where Quantity_Available>=1'
    command(st0)
    fetch()
    book_selected = input('Enter name of book from above list : ')
    borrowers_name = input('Enter Borrower Name : ')
    contact = input('Enter contact no. : ')
    st_insert = "INSERT INTO borrower (borrowers_name, book_lent, contact_no) VALUES ('%s', '%s', %s)" % (borrowers_name, book_selected, contact)
    command(st_insert)
    st_dec='update books set quantity_available = quantity_available - 1 where book_name="{}"'.format(book_selected)
    command(st_dec)
    print('%s successfully lent to %s' % (book_selected, borrowers_name))

def close():
    mycon.commit()
    mycon.close()
    if mycon.is_connected():
        print('still connected to localhost')
    else:
        print('\n\nconnection closed successfully.')
    sys.exit()


msg = '''
#### WELCOME TO LIBRARY MANAGEMENT SYSTEM ####

1. View details of all available Books
2. Add new books
3. Lend a book
4. View details of borrowers
5. Exit
Enter your choice: '''

while True:
    dec = input(msg)
    if dec == '1':
        all_data('books')
    elif dec=='2':
        add_book()
    elif dec == '3':
        lend()
    elif dec=='4':
        all_data('borrower')
    elif dec=='5':
        close()
    else:
        print('Please enter a valid choice')

