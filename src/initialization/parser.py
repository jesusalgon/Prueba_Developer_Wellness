# Imports
import pandas as pd

# Constants and global variables
MONTHS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
          'Nov': 11, 'Dec': 12}


def add_zero_padding_to_single_number(number):
    number = str(number)
    if len(number) == 1:
        number = '0' + number

    return number


def convert_month_into_number(month):
    return add_zero_padding_to_single_number(MONTHS[month])


def format_date_and_time(data):
    new_date_col = []
    new_time_col = []
    date_col = list(data.loc[:, 'Date'])
    for index in range(len(date_col)):
        date = date_col[index]
        parts = date.split()
        day = add_zero_padding_to_single_number(parts[0])
        month = convert_month_into_number(parts[1])
        year = parts[2]
        time = parts[3]

        new_date_col.append(f'{year}-{month}-{day}')
        new_time_col.append(time)
    data = data.assign(Date=new_date_col)
    data.insert(loc=1, column='Time', value=new_time_col)

    return data


def parse_data(data):
    data = data.dropna()
    data.reset_index(inplace=True, drop=True)
    data = format_date_and_time(data)

    return data