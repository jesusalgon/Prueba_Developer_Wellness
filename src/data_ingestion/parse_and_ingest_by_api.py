# Imports
import pandas as pd
from parser import parse_data
import requests


# Constants and global variables
CSV_PATH = '../../data/csv/Monitoring report.csv'
API_ENDPOINT = 'http://127.0.0.1:8000/data/'


def post_row(row):
    data = {
        'date': row[0],
        'time': row[1],
        'energy': row[2],
        'reactive_energy': row[3],
        'power': row[4],
        'maximeter': row[5],
        'reactive_power': row[6],
        'voltage': row[7],
        'intensity': row[8],
        'power_factor': row[9]
    }
    response = requests.post(API_ENDPOINT, data)


if __name__ == '__main__':
    raw_data = pd.read_csv(CSV_PATH)
    parsed_data = parse_data(raw_data)
    for _, row in parsed_data.iterrows():
        post_row(list(row))

