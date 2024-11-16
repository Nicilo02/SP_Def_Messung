import pandas as pd
import sqlite3
import numpy as np

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


