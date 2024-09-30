import os
import csv
import datetime
from urllib.parse import urlunparse, urlencode

days = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"]
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

    bread_csv = []
    current_year = datetime.datetime.now().year
    current_date = None
    weekly_season = None
    weekly_theme = None
    for bread_line in bread_lines:
        first_word_is_day = bread_line[:3] in days or bread_line[:4] in days or bread_line[:5] in days
        row_has_date = bread_line[0].isdigit()
        if not first_word_is_day and not row_has_date:
            weekly_theme = bread_line.strip()
        elif bread_line.split(": ")[0] not in days:  # then it's a string with format "MM.DD, <season>"
            date_string, season = bread_line.split(", ")

            month, date = list(map(int, date_string.split(".")))
            current_date = datetime.datetime(current_year, month, date)
            weekly_season = season 
        else:
            day_of_week, verse = bread_line.split(": ")
            if not day_of_week == "Sun":
                current_date += datetime.timedelta(days=1)
            print(current_date.date(), verse, get_bible_gateway_url(verse), weekly_season, weekly_theme)
            # add in biblegateway verse
            link = get_bible_gateway_url(verse)
            bread_csv.append([current_date.date(), verse, link, weekly_season, weekly_theme])
    
    return bread_csv

def write_csv(path, bread_csv):
    # turn it all into a CSV
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header row
        writer.writerow(['date', 'verse', 'link', 'season', 'theme'])
        # Write the dictionary data row by row
        for row in bread_csv:
            writer.writerow(row)

if __name__ == "__main__":
    # Construct the absolute path to the bread.txt file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'bread.txt')
    bread_csv = transformText(file_path)
    write_csv(os.path.join(script_dir, 'verses.csv'), bread_csv)