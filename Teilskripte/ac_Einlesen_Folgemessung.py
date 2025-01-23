import pandas as pd

def read_csv_folge(file_path_folge):
    data_folge = pd.read_csv(file_path_folge)
    print(data_folge.head())  # Zeigt die ersten Zeilen an
    return data_folge

def add_header_to_csv_folge(file_path_folge):
    # Die gewünschte Kopfzeile festlegen
    desired_header_folge = ['Punktnummer', 'X', 'Y', 'Z', 'Objektcode']

    # CSV-Datei lesen (automatische Erkennung der Kopfzeile)
    first_row_folge = pd.read_csv(file_path_folge, nrows=1)  # Nur die erste Zeile einlesen

    # Überprüfung, ob die Datei bereits eine Kopfzeile hat
    if list(first_row_folge.columns) == desired_header_folge:
        print("Die Datei enthält bereits die korrekte Kopfzeile.")
        keep_header_folge = input("Möchten Sie die vorhandene Kopfzeile behalten? (ja/nein): ").strip().lower()
        if keep_header_folge == 'ja':
            print("Die Kopfzeile bleibt unverändert.")
            return
        else:
            print("Die Kopfzeile wird ersetzt.")
    else:
        print("Die Datei hat entweder keine oder eine falsche Kopfzeile.")

    # Datei ohne Kopfzeile einlesen (falls nötig)
    current_data_folge = pd.read_csv(file_path_folge, header=0 if list(first_row_folge.columns) == desired_header_folge else None)

    # Wenn die Spaltenanzahl nicht übereinstimmt, Fehlermeldung ausgeben und Werte ergänzen
    if current_data_folge.shape[1] == len(desired_header_folge) - 1:
        # Eine Spalte fehlt (Objektcode fehlt), also fügen wir diese hinzu
        specific_value = input("Welchen Wert sollte der Objektcode haben? ").strip()
        current_data_folge['Objektcode'] = specific_value
        
    elif current_data_folge.shape[1] != len(desired_header_folge):
        print("Fehler: Die Datei hat eine falsche Anzahl an Spalten. Es können keine Änderungen vorgenommen werden.")
        return

    # Kopfzeile hinzufügen oder überschreiben
    current_data_folge.columns = desired_header_folge

    # Abfrage für den Dateinamen der Ausgabedatei
    output_file_folge = input("Wie soll die neue Datei heißen? ") or "output_with_new_header.csv"

    # Datei mit neuer Kopfzeile speichern
    current_data_folge.to_csv(output_file_folge, index=False)
    print(f"CSV-Datei mit neuer Kopfzeile wurde unter {output_file_folge} gespeichert.")
    