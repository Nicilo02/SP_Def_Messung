import pandas as pd

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
check_csv = '100.csv'  # Pfad zur CSV-Datei, die überprüft werden soll
result = check_header_case(check_csv)

