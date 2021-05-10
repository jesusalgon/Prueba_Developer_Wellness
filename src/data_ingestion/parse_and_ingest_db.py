# Imports
import pandas as pd
import sqlite3
from parser import parse_data

# Constants and global variables
CSV_PATH = '../../data/csv/Monitoring report.csv'
DB_PATH = '../django_api/wellness.db'


def create_db():
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS electricity_consumption (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                energy REAL NOT NULL,
                reactive_energy REAL NOT NULL,
                power REAL NOT NULL,
                maximeter REAL NOT NULL,
                reactive_power REAL NOT NULL,
                voltage REAL NOT NULL,
                intensity REAL NOT NULL,
                power_factor REAL NOT NULL
            );
        ''')


def ingest_db(data):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for _, row in data.iterrows():
        row = list(row)
        date = row[0]
        time = row[1]
        energy = row[2]
        reactive_energy = row[3]
        power = row[4]
        maximeter = row[5]
        reactive_power = row[6]
        voltage = row[7]
        intensity = row[8]
        power_factor = row[9]

        cursor.execute(f'''
            INSERT INTO electricity_consumption (date, time, energy, reactive_energy, power, maximeter, 
                reactive_power, voltage, intensity, power_factor)
            SELECT
                "{date}", "{time}", {energy}, {reactive_energy}, {power}, {maximeter}, {reactive_power}, {voltage}, 
                {intensity}, {power_factor}
            EXCEPT
                SELECT
                    date, time, energy, reactive_energy, power, maximeter, reactive_power, voltage, intensity, 
                    power_factor
                FROM electricity_consumption
                WHERE
                    date="{date}" AND time="{time}" AND energy={energy} AND reactive_energy={reactive_energy} 
                    AND power={power} AND maximeter={maximeter} AND reactive_power={reactive_power} 
                    AND voltage={voltage} AND intensity={intensity} AND power_factor={power_factor};
        ''')

    connection.commit()
    connection.close()


if __name__ == '__main__':
    raw_data = pd.read_csv(CSV_PATH)
    parsed_data = parse_data(raw_data)
    create_db()
    ingest_db(parsed_data)
