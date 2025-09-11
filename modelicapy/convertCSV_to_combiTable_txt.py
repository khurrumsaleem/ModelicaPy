# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 13:45:08 2024

@author: fig
"""
import pandas as pd
import os

def convert_csv_to_txt(filename, exclude_first_col=True):
    # Read the csv
    df = pd.read_csv(filename)
    
    # Get columns names
    column_names = list(df.columns)
    if exclude_first_col:
        column_names = column_names[1:]
        df = df.iloc[:, 1:]
    
    # Write DataFrame to text file in the required format
    with open(list(os.path.splitext(filename))[0] + '.txt', 'w') as fil:
        fil.write('#1\n')
        fil.write(f'double table({df.shape[0]}, {df.shape[1]}) # {" ".join(column_names)}\n')
        
        for _, row in df.iterrows():
            fil.write(f'{" ".join([str(row[col]) for col in column_names])}\n')
    return df

if __name__ == "__main__":
    filename = r'resources\example_timeseries_scaled.csv'
    convert_csv_to_txt(filename)