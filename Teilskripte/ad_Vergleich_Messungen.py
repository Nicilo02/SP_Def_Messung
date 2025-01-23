import pandas as pd
import sqlite3

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
    merged_data['x_diff'] = merged_data['x_New'] - merged_data['x_Null']
    merged_data['y_diff'] = merged_data['y_New'] - merged_data['y_Null']
    merged_data['z_diff'] = merged_data['z_New'] - merged_data['z_Null']

    # 6. Differenzen auf 4 Dezimalstellen runden
    merged_data['x_diff'] = merged_data['x_diff'].round(4)
    merged_data['y_diff'] = merged_data['y_diff'].round(4)
    merged_data['z_diff'] = merged_data['z_diff'].round(4)

    # 7. Ergebnis speichern oder anzeigen
    result = merged_data[['Punktnummer', 'x_diff', 'y_diff', 'z_diff']]
    print("Berechnete Differenzen:")
    print(result)

    # Optional: Speichern der Ergebnisse in eine CSV-Datei
    result.to_csv(output_path, index=False)
    print(f"\nDie Differenzen wurden in '{output_path}' gespeichert.")

    # 8. Datenbankverbindung schließen
    conn.close()
