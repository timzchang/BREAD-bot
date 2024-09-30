import os
import csv
import datetime
from urllib.parse import urlunparse, urlencode

days = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"]

def clean_bread_lines(bread_lines):
    bread_lines_clean = []
    for row in bread_lines:
        first_word_is_day = row[:3] in days or row[:4] in days
        row_has_date = row[0].isdigit()
        if first_word_is_day or row_has_date:
            bread_lines_clean.append(row)
    return bread_lines_clean

def get_bible_gateway_url(verse):
    query_params = urlencode({
        "search": verse,
        "version": "NIV"
    })
    return urlunparse(('https', 'www.biblegateway.com', '/passage/', '', query_params, ''))

def transformText(file_path):
    #get text from bread file and split into lines
    with open(file_path, 'r') as file:
        data = file.read()
    bread_lines = data.splitlines()
    #remove lines with just themes
    bread_lines_clean = clean_bread_lines(bread_lines)

    bread_csv = []
    current_year = datetime.datetime.now().year
    current_date = None
    for bread_line in bread_lines_clean:
        if bread_line.split(": ")[0] not in days:  # then it's a string with format "MM.DD, <Theme>"
            date_string = bread_line.split(", ")[0]

            month, date = list(map(int, date_string.split(".")))
            current_date = datetime.datetime(current_year, month, date)
        else:
            day_of_week, verse = bread_line.split(": ")
            if not day_of_week == "Sun":
                current_date += datetime.timedelta(days=1)
            print(current_date.date(), verse, get_bible_gateway_url(verse))
            # add in biblegateway verse
            link = get_bible_gateway_url(verse)
            bread_csv.append([current_date.date(), verse, link])
    
    return bread_csv

def write_csv(path, bread_csv):
    # turn it all into a CSV
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header row
        writer.writerow(['date', 'verse', 'link'])
        # Write the dictionary data row by row
        for row in bread_csv:
            writer.writerow(row)

if __name__ == "__main__":
    # Construct the absolute path to the bread.txt file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'bread.txt')
    bread_csv = transformText(file_path)
    write_csv(os.path.join(script_dir, 'verses.csv'), bread_csv)