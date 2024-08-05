# coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import sys


# check numbers of working stations
def stations_check():
    folder_path = 'data/data_small'
    numbers = []
    pattern = re.compile(r'^TG_STAID0+(\d+)\.txt$')

    # Iterate over files in the specified folder
    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            number = match.group(1)
            numbers.append(number)
    return numbers


def preparing_data(station_id):
    file_path = f"data/data_small/TG_STAID{station_id:06d}.txt"

    try:
        df = pd.read_csv(file_path, skiprows=20, parse_dates=["    DATE"])

        df['TGN'] = df['   TG'].mask(df['   TG'] == -9999, np.nan)
        df['TG'] = df['TGN'] / 10
        del df['TGN']

        df.rename(columns={'    DATE': 'DATE'}, inplace=True)

        start_date = df['DATE'].min()
        end_date = df['DATE'].max()

    except Exception as e:
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e.args[0]}")
        start_date = end_date = df = "No data"
    return start_date, end_date, df


def check_api(date, station):
    start_date, end_date, df = preparing_data(station)
    if start_date != "No data":
        my_data = df.loc[(df['DATE'] == date) & (df['STAID'] == station)]
        # print("dataZH \n ==== \n", my_data)
        # print("start = ", start_date, " end=", end_date)
        return str(my_data['TG'].squeeze())
    return start_date
