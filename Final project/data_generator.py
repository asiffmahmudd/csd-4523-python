import csv
import random
import time

year = 1900

fieldnames = ["year", "inflation"]

with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
    csv_writer.writeheader()

while True:
    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        inflation = round(random.uniform(0, 100), 2)
        info = {
            "year" : year,
            "inflation" : inflation
        }
        
        csv_writer.writerow(info)
        print(year, inflation)

        year += 1
    
    if(year == 1940):
        year = 1900
        filename = "data.csv"
        # opening the file with w+ mode truncates the file
        f = open(filename, "w+")
        f.close()
        with open('data.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
            csv_writer.writeheader()

    time.sleep(0.5)