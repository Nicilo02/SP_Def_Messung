import os
import pandas as pd
import sqlite3
from Teilskripte.aa_Teil_1_csv import read_csv, add_header_to_csv # Importieren der Funktion aus dem externen Skript
from Teilskripte.ac_Einlesen_Folgemessung import read_csv_folge, add_header_to_csv_folge


def main():
    # Beispiel-Dateipfad
    file_path = 'Excelfiles/Nullmessung.csv'
    
    # Die Funktion add_header_to_csv aufrufen, um die Kopfzeile hinzuzufügen
    add_header_to_csv(file_path)
    
    # CSV-Daten nach dem Hinzufügen der Kopfzeile einlesen
    data1 = read_csv(file_path)
    
    output_file = input("Geben Sie den Namen der Ausgabedatei ein: ") or "output_with_new_header.csv"
    
    return data1, output_file

    
if __name__ == "__main__":
    data1, output_file = main()
    
    print(data1)
    
def check_header_case(check_csv):
    """
    Überprüft, ob die Header einer CSV-Datei den erwarteten Werten entsprechen und ob sie großgeschrieben sind.

    :param file_path: Der Pfad zur CSV-Datei
    :return: True, wenn alle Header korrekt und großgeschrieben sind, sonst False
    """
    try:
        # Lade nur die Kopfzeile der CSV-Datei
        header = pd.read_csv(check_csv, nrows=0).columns.tolist()

        # Definiere den erwarteten Header (großgeschrieben)
        expected_header = ['Punktnummer', 'X', 'Y', 'Z', 'Objektcode']

        # Überprüfen, ob die Header übereinstimmen und ob sie großgeschrieben sind
        if header == expected_header:
            print("Die Header sind korrekt und großgeschrieben.")
            return True
        else:
            print(f"Fehler: Die Header stimmen nicht überein.\n"
                  f"Gefundene Header: {header}\nErwartete Header: {expected_header}")
            return False

    except Exception as e:
        print(f"Fehler beim Verarbeiten der Datei: {e}")
        return False


# Beispielaufruf der Funktion
check_csv = output_file  # Pfad zur CSV-Datei, die überprüft werden soll
result = check_header_case(check_csv)
    

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
            X REAL,
            Y REAL,
            Z REAL,
            Objektcode TEXT
        )
    ''')
    conn.commit()
    return conn

def save_data_to_db(conn, data):
    cursor = conn.cursor()
    for _, row in data.iterrows():
        cursor.execute('''
            INSERT INTO messungen (Punktnummer, X, Y, Z, Objektcode)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['Punktnummer'], row['X'], row['Y'], row['Z'], row['Objektcode']))
    conn.commit()
    print('Daten erfolgreich in die Datenbank gespeichert.')

file_path = output_file
data = read_csv(file_path)
conn = create_database()
save_data_to_db(conn, data)
conn.close()

def main():
    # Beispiel-Dateipfad
    file_path_folge = input('Was ist der Name der Zweiten Datei? ')
    
    # Die Funktion add_header_to_csv aufrufen, um die Kopfzeile hinzuzufügen
    add_header_to_csv_folge(file_path_folge)
    
    # CSV-Daten nach dem Hinzufügen der Kopfzeile einlesen
    data_folge = read_csv_folge(file_path_folge)
    
    output_file_folge = input("Geben Sie den Namen der Ausgabedatei ein: ") or "output_with_new_header.csv"
    
    return data_folge, output_file_folge
    
if __name__ == "__main__":
    data_folge, output_file_folge = main()
    
    print(data_folge)
    
    
def check_header_case(check_csv_2):
    """
    Überprüft, ob die Header einer CSV-Datei den erwarteten Werten entsprechen und ob sie großgeschrieben sind.

    :param file_path: Der Pfad zur CSV-Datei
    :return: True, wenn alle Header korrekt und großgeschrieben sind, sonst False
    """
    try:
        # Lade nur die Kopfzeile der CSV-Datei
        header = pd.read_csv(check_csv_2, nrows=0).columns.tolist()

        # Definiere den erwarteten Header (großgeschrieben)
        expected_header = ['Punktnummer', 'X', 'Y', 'Z', 'Objektcode']

        # Überprüfen, ob die Header übereinstimmen und ob sie großgeschrieben sind
        if header == expected_header:
            print("Die Header sind korrekt und großgeschrieben.")
            return True
        else:
            print(f"Fehler: Die Header stimmen nicht überein.\n"
                  f"Gefundene Header: {header}\nErwartete Header: {expected_header}")
            return False

    except Exception as e:
        print(f"Fehler beim Verarbeiten der Datei: {e}")
        return False


# Beispielaufruf der Funktion
check_csv_2 = output_file_folge  # Pfad zur CSV-Datei, die überprüft werden soll
result = check_header_case(check_csv_2)
    
    
def berechne_differenzen(db_path, data_new_path, output_path):
    # 1. Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(db_path)

    # 2. Abfrage durchführen, um die Nullmessung zu laden
    nullmessung_query = "SELECT * FROM messungen"  # Ändere 'messungen' je nach Tabellennamen
    nullmessung = pd.read_sql_query(nullmessung_query, conn)

    # 3. Zweite CSV-Datei laden
    data_new = pd.read_csv(data_new_path)

    # 4. DataFrames anhand von Punktnummer verbinden (inner join)
    merged_data = pd.merge(nullmessung, data_new, on='Punktnummer', suffixes=('_Null', '_New'))

    # 5. Differenzen berechnen
    merged_data['X_diff'] = merged_data['X_New'] - merged_data['X_Null']
    merged_data['Y_diff'] = merged_data['Y_New'] - merged_data['Y_Null']
    merged_data['Z_diff'] = merged_data['Z_New'] - merged_data['Z_Null']

    # 6. Differenzen auf 4 Dezimalstellen runden
    merged_data['X_diff'] = merged_data['X_diff'].round(3)
    merged_data['Y_diff'] = merged_data['Y_diff'].round(3)
    merged_data['Z_diff'] = merged_data['Z_diff'].round(3)

    # 7. Ergebnis speichern oder anzeigen
    result = merged_data[['Punktnummer', 'X_diff', 'Y_diff', 'Z_diff']]
    print("Berechnete Differenzen:")
    print(result)

    # Optional: Speichern der Ergebnisse in eine CSV-Datei
    result.to_csv(output_path, index=False)
    print(f"\nDie Differenzen wurden in '{output_path}' gespeichert.")

    # 8. Datenbankverbindung schließen
    conn.close()
    
db_path = 'Defmes_data.db'
data_new_path = output_file_folge
output_path = 'Differenzen.csv'

berechne_differenzen(db_path, data_new_path, output_path)




