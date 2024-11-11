import pandas as pd
import sqlite3
import csv
import numpy as np

def read_csv(file_path):
    data= pd.read_csv(file_path)
    return data

def shift_data(data):
    shifted_data = data.shift(1)
    return shifted_data

def save_csv(data, output_file):
    data.to_csv(output_file, index=False)
    
file_path = '0_Messung_240315_4Stellen.csv'
data = read_csv(file_path)

shifted_data = shift_data(data)

output_file = 'Test.csv'
save_csv(shifted_data, output_file)