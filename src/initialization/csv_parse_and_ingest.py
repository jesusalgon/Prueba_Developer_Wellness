# Imports
import pandas as pd
import sqlite3

# Constants and global variables
CSV_PATH = '../../data/csv/Monitoring report.csv'
DB_PATH = '../../data/databases/wellness.db'
MONTHS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
          'Nov': 11, 'Dec': 12}


def add_zero_padding_to_single_number(number):
    number = str(number)
    if len(number) == 1:
        number = '0' + number

    return number


def convert_month_into_number(month):
    return add_zero_padding_to_single_number(MONTHS[month])


def format_date(data):
    date_col = list(data.loc[:, 'Date'])
    for index in range(len(date_col)):
        date = date_col[index]
        parts = date.split()
        day = add_zero_padding_to_single_number(parts[0])
        month = convert_month_into_number(parts[1])
        year = parts[2]
        hour = parts[3]

        date_col[index] = f'{year}-{month}-{day} {hour}'
    data = data.assign(Date=date_col)

    return data


def parse_data(data):
    data = data.dropna()
    data.reset_index(inplace=True, drop=True)
    data = format_date(data)

    return data


def create_db():
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS electricity_consumption (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT NOT NULL,
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
        datetime = row[0]
        energy = row[1]
        reactive_energy = row[2]
        power = row[3]
        maximeter = row[4]
        reactive_power = row[5]
        voltage = row[6]
        intensity = row[7]
        power_factor = row[8]

        cursor.execute(f'''
            INSERT INTO electricity_consumption (datetime, energy, reactive_energy, power, maximeter, 
                reactive_power, voltage, intensity, power_factor)
            SELECT
                "{datetime}", {energy}, {reactive_energy}, {power}, {maximeter}, {reactive_power}, {voltage}, 
                {intensity}, {power_factor}
            EXCEPT
                SELECT
                    datetime, energy, reactive_energy, power, maximeter, reactive_power, voltage, intensity, 
                    power_factor
                FROM electricity_consumption
                WHERE
                    datetime="{datetime}" AND energy={energy} AND reactive_energy={reactive_energy} AND power={power}
                    AND maximeter={maximeter} AND reactive_power={reactive_power} AND voltage={voltage}
                    AND intensity={intensity} AND power_factor={power_factor};
        ''')

    connection.commit()
    connection.close()


if __name__ == '__main__':
    raw_data = pd.read_csv(CSV_PATH)
    parsed_data = parse_data(raw_data)
    create_db()
    ingest_db(parsed_data)
