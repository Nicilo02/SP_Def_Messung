import pandas as pd
import sqlite3
import csv
import numpy as np

#Funktioniert ab hier:
def read_csv():
    data = pd.read_csv('0_Messung_240315_4Stellen.csv')
    print (data)
    return data




def read_csv(file_path):
    data = pd.read_csv(file_path)
    return data

def create_database():
    conn = sqlite3.connect('Defmes_data.db')
    cursor = conn.cursor ()
    cursor.execute ('''
        CREATE TABLE IF NOT EXISTS messungen (
            id INTEGER PRIMARY KEY,
            punktnummer TEXT,
            x REAL,
            y REAL,
            z REAL,
            objektcode TEXT
        )
    ''')
    conn.commit()
    return conn

def save_data_to_db(conn, data):
    cursor = conn.cursor ()
    for _, row in data.iterrows():
        cursor.execute('''
            INSERT INTO messungen (punktnummer, x, y, z, objektcode)
            VALUES (?, ?, ?, ?, ?)
        ''',(row['Punktnummer'],row['x'],row['y'],row['z'],row['Objektcode']))
    conn.commit()
    print('Daten erfolgreich in die Datenbank gespeichert.')
    
file_path = '0_Messung_240315_4Stellen.csv'
data = read_csv(file_path)
print (data.head())

conn = create_database()
save_data_to_db(conn, data)

conn.close()