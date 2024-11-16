import pandas as pd

def read_csv(file_path):
    data = pd.read_csv(file_path)
    print(data.head())  # Zeigt die ersten Zeilen an
    return data

def add_header_to_csv(file_path):
    # Die gewünschte Kopfzeile festlegen
    desired_header = ['Punktnummer', 'X', 'Y', 'Z', 'Objektcode']

    # CSV-Datei lesen (automatische Erkennung der Kopfzeile)
    first_row = pd.read_csv(file_path, nrows=1)  # Nur die erste Zeile einlesen

    # Überprüfung, ob die Datei bereits eine Kopfzeile hat
    if list(first_row.columns) == desired_header:
        print("Die Datei enthält bereits die korrekte Kopfzeile.")
        keep_header = input("Möchten Sie die vorhandene Kopfzeile behalten? (ja/nein): ").strip().lower()
        if keep_header == 'ja':
            print("Die Kopfzeile bleibt unverändert.")
            return
        else:
            print("Die Kopfzeile wird ersetzt.")
    else:
        print("Die Datei hat entweder keine oder eine falsche Kopfzeile.")

    # Datei ohne Kopfzeile einlesen (falls nötig)
    current_data = pd.read_csv(file_path, header=0 if list(first_row.columns) == desired_header else None)

    # Wenn die Spaltenanzahl nicht übereinstimmt, Fehlermeldung ausgeben und Werte ergänzen
    if current_data.shape[1] != len(desired_header):
        print(f"Fehler: Die Datei muss {len(desired_header)} Spalten enthalten.")
        specific_value = input("Welchen Wert sollte der Objektcode haben? ").strip()
        
        # Objektcode hinzufügen, falls er fehlt
        if current_data.shape[1] == len(desired_header) - 1:  # Eine Spalte fehlt
            current_data['Objektcode'] = specific_value
        else:
            print("Die Struktur der Datei ist nicht kompatibel.")
            return

    # Kopfzeile hinzufügen oder überschreiben
    current_data.columns = desired_header

    # Abfrage für den Dateinamen der Ausgabedatei
    output_file = input("Wie soll die neue Datei heißen? ") or "output_with_new_header.csv"

    # Datei mit neuer Kopfzeile speichern
    current_data.to_csv(output_file, index=False)
    print(f"CSV-Datei mit neuer Kopfzeile wurde unter {output_file} gespeichert.")
