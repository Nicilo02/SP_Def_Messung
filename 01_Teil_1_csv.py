import pandas as pd

def add_header_to_csv(file_path):
    # Die gewünschte Kopfzeile festlegen
    desired_header = ['Punktnummer', 'X', 'Y', 'Z',]
    
    # CSV-Datei ohne Kopfzeile einlesen
    current_data = pd.read_csv(file_path, header=None)
    
    if current_data.shape[1] != 5:
        print('Fehler: Die Datei muss 5 Spalten enthalten')
        
        specific_value = input('Welchen Wert sollte der Objektcode haben?')
        
        current_data['Neuer_Wert'] = specific_value
        
        current_data.columns = desired_header + ['Objektcode']
        
    else:    
        # Die Kopfzeile zu den Daten hinzufügen
        current_data.columns = desired_header
        
    # Abfrage für den Dateinamen der Ausgabedatei
    output_file = input('Wie soll die neue Datei heißen? ') or 'output_with_new_header.csv'
    
    # Datei mit neuer Kopfzeile speichern
    current_data.to_csv(output_file, index=False)
    print(f'CSV-Datei mit neuer Kopfzeile unter: {output_file}')

# Beispiel-Dateipfad
file_path = '240730_Folgemess.csv'
add_header_to_csv(file_path)
