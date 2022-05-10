import pyodbc
import pandas as pd
import sys

server = 'DESKTOP-A2BF0RR\SQLEXPRESS'
database = 'CryptoCurrency'
username = 'crypto_api'
password = ''


def insert(c):
    c.execute('SELECT @@version;')
    row = c.fetchone()
    print(row)

def drop(c, table):
    try:
        c.execute(f'DROP TABLE {table}')
    except:
        print(f"Can't drop table: {table}")

def create_general(c):
    try:
        c.execute('CREATE Table General(ID varchar(30), Symbol varchar(10), Name varchar(255), Market_cap money)')
        print('General table was created.')
    except:
        print("Can't create table: General")

def create_historical(c):
    try:
        c.execute('CREATE Table Historical(ID varchar(30), PriceDate Date, Price money)')
        print('Historical table was created.')
    except:
        print("Can't create table: Historical") 

def get_cred(user):
    print(f'Password to {user} user: ')
    password = input()
    
def insert_general(c):
    data = pd.read_csv('general_data.csv', sep=';')
    del data['Unnamed: 0']

    for index, row in data.iterrows():
     cursor.execute("INSERT INTO General (ID, Symbol, Name, Market_cap) values(?,?,?,?)", row.id, row.symbol, row['name'], row.market_cap)
    print("Inserted data into General table")

def insert_historical(c):
    data = pd.read_csv('historical_data.csv', sep=';')
    del data['Unnamed: 0']

    for index, row in data.iterrows():
     cursor.execute("INSERT INTO Historical (ID, PriceDate, Price) values(?,?,?)", row.id, row.date, row.price)
    print("Inserted data into Historical table")

print('You want insert data to database? (Y/N): ')
val = input()
if val == 'Y' or val =='y':
    get_cred(username)
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password,Trusted_Connection='Yes')
    cursor = cnxn.cursor()
    print('Connected.')

    drop(cursor, 'General')
    create_general(cursor)

    drop(cursor, 'Historical')
    create_historical(cursor)

    insert_general(cursor)
    insert_historical(cursor)

    cnxn.commit()
    print("Comitted")

if val == 'N' or val =='n':
    sys.exit()


if __name__ == '__main__':
    print('Started module.')