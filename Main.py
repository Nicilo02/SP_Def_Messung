##To-Do
import pandas as pd
import sqlite3
import csv
import numpy as np

def add_header_to_csv(file_path):
    desired_header = ['Punktnummer','X','Y','Z','Objektcode']
    
    current_data = pd.read_csv(file_path)
    current_header = list(current_data.columns)
    
    output_file = input('Wie soll die neue Datei heissen')
    
    if current_header == desired_header:
        print('Kopfzeile ist bereits vorhanden. Keine Änderung erforderlich')
        
        current_data.to_csv(output_file, index=False)
    
    else:
        print('Die Kopfzeile fehlt. Neue Kopfzeile wird eingefügt')
        
        new_header = pd.DataFrame(columns=desired_header)
        empty_row = pd.DataFrame([['' for _ in desired_header]], columns = desired_header)
        data_with_header = pd.concat([new_header, empty_row,  current_data], ignore_index= True)
        data_with_header.to_csv(output_file, index=False)
        print(f'CSV-Datei mit neuer Kopfzeile gespeichert unter: {output_file}')

    
file_path = '0_Messung_240315_4Stellen.csv'

add_header_to_csv(file_path)