import csv 

def csv_add_rows(filename, data, fieldnames, write_fieldnames=False, mode='a'):
    
    if write_fieldnames:
        with open(filename, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()

    with open(filename, mode) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        for row in data:
            writer.writerow(row)