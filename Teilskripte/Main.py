##To-Do


##Done
# Import Nullmessung CSV mit Kopfzeile funktioniert

import pandas as pd
import sqlite3

def read_csv(file_path):
    data = pd.read_csv(file_path)
    print(data.head())  # Zeigt die ersten Zeilen an
    return data

def create_database():
    conn = sqlite3.connect('Defmes_data.db')
    cursor = conn.cursor()
    cursor.execute('''
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
    cursor = conn.cursor()
    for _, row in data.iterrows():
        cursor.execute('''
            INSERT INTO messungen (punktnummer, x, y, z, objektcode)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['Punktnummer'], row['X'], row['Y'], row['Z'], row['Objektcode']))
    conn.commit()
    print('Daten erfolgreich in die Datenbank gespeichert.')

file_path = 'Test_001.csv'  # Stelle sicher, dass der Pfad korrekt ist
data = read_csv(file_path)
conn = create_database()
save_data_to_db(conn, data)
conn.close()
