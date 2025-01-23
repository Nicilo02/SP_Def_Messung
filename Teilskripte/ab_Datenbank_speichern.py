import pandas as pd
import sqlite3
import numpy as np

def read_csv(file_path):
    data = pd.read_csv(file_path)
    print(data.head())  # Zeigt die ersten Zeilen an
    return data

def create_database():
    conn = sqlite3.connect('Defmes_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messungen (
            Punktnummer TEXT,
            x REAL,
            y REAL,
            z REAL,
            objektcode TEXT
        )
    ''')
    conn.commit()
    return conn

def save_data_to_db(conn, data_new):
    cursor = conn.cursor()
    for _, row in data_new.iterrows():
        cursor.execute('''
            INSERT INTO messungen (Punktnummer, x, y, z, objektcode)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['Punktnummer'], row['x'], row['y'], row['z'], row['objektcode']))
    conn.commit()
    print('Daten erfolgreich in die Datenbank gespeichert.')

file_path = '123.csv'  # Stelle sicher, dass der Pfad korrekt ist
data = read_csv(file_path)
conn = create_database()
save_data_to_db(conn, data)
conn.close()
