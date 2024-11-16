import pandas as pd
import sqlite3

# Funktion zum Laden der Ursprungsdaten aus der SQLite-Datenbank
def load_original_data():
    conn = sqlite3.connect('Defmes_data.db')
    query = "SELECT punktnummer, x, y, z FROM messungen"
    original_data = pd.read_sql_query(query, conn)
    conn.close()
    return original_data

# Funktion zum Berechnen der Differenzen
def calculate_differences(new_data_path):
    # Neue CSV-Datei ohne Kopfzeile laden, explizite Spaltennamen angeben
    new_data = pd.read_csv(new_data_path)
    
    # Ursprungsdaten aus der Datenbank laden
    original_data = load_original_data()

    # DataFrames anhand von 'Punktnummer' verbinden (inner join)
    merged_data = pd.merge(original_data, new_data, on='Punktnummer', suffixes=('_orig', '_new'))

    # Differenzen berechnen
    merged_data['X_diff'] = merged_data['X_new'] - merged_data['X_orig']
    merged_data['Y_diff'] = merged_data['Y_new'] - merged_data['Y_orig']
    merged_data['Z_diff'] = merged_data['Z_new'] - merged_data['Z_orig']

    return merged_data[['Punktnummer', 'X_diff', 'Y_diff', 'Z_diff']]

# Hauptprogramm
new_data_path = 'Folgemessung_1.csv'  # Pfad zur neuen CSV-Datei ohne Kopfzeile
differences = calculate_differences(new_data_path)

# Differenzen anzeigen
print(differences)

# Optional: Differenzen in eine neue CSV-Datei speichern
differences.to_csv('differenzen.csv', index=False)


