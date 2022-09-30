#!/usr/bin/python

import os
from os.path import exists
import petl as etl

def extract():
    # Extract data from a CSV file
    return etl.fromcsv('../chinook/Customer.csv')

def transform(data):
    # Transform data
    return (data
            .convert('CustomerId', int)
            .addfield('CustomerName', lambda rec: rec['FirstName'] + ' ' + rec['LastName'])
            .cut('CustomerId', 'CustomerName', 'Address', 'City', 'Country')
            .sort('Country'))
    
def load(data):
    # Load data into a CSV file
    # Check if the file already exists
    if exists('CustomerTransformed.csv'):
        print('File already exists')
        print('Do you want to overwrite it?')
        answer = input('y/n: ')
        if answer == 'y':
            os.remove('CustomerTransformed.csv')
            etl.tocsv(data, 'CustomerTransformed.csv')
            print('File overwritten')
            return
        else:
            print('File not overwritten')
            return
    else:
        etl.tocsv(data, 'CustomerTransformed.csv')
    return

def main():
    data = extract()
    data = transform(data)
    load(data)

if __name__ == '__main__':
    main()
