## Python ETL Pipeline with PETL

### ETL Objective
1. Extract data from a dataset (Customer.csv)

2. Transform data with these objectives:
- Remove unnecessary columns
- Concatenate first and last name into one column
- Select only customers from the United Kingdom

3. Load data into a new dataset (CustomerTransformed.csv)

### Overview
The overview of the ETL process in `main.py` is as follows:
```python
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
```

***

<p align="center"><i>This repository is only for educational purpose.</i></p>