import os
import datetime

days = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"]
def clean_bread_lines(bread_lines):
    #remove lines with just themes
    bread_lines_clean = []
    for row in bread_lines:
        print(row)
        print(row[:3], row[:4])
        print(row[:3] in days, row[:4] in days)
        if row[:3] in days or row[:4] in days or row[0].isdigit():
            bread_lines_clean.append(row)
    return bread_lines_clean

def transformText():
    # Get the absolute path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the absolute path to the bread.txt file
    file_path = os.path.join(script_dir, 'bread.txt')
    #get text from bread file and split into lines
    with open(file_path, 'r') as file:
        data = file.read()
    bread_lines = data.splitlines()
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    #remove lines with just themes
    bread_lines_clean = clean_bread_lines(bread_lines)

    print(bread_lines_clean)

    bread_csv = []
    current_year = datetime.datetime.now().year
    current_date = None
    for bread_line in bread_lines_clean:
        if bread_line.split(": ")[0] not in days:
            date_string = bread_line.split(", ")[0]
            print("this is a date", date_string)

            month, date = list(map(int, date_string.split(".")))
            current_date = datetime.datetime(current_year, month, date)
            # print(current_date)
        else:
            print("this is a verse")
            day_of_week, verse = bread_line.split(": ")
            # print(current_date, verse)
            if not day_of_week == "Sun":
                current_date += datetime.timedelta(days=1)
            print(current_date, day_of_week, verse)
            bread_csv.append([current_date, day_of_week, verse])

        # build a new array
        # if a line.split(": ").first is not a day_of_week, then it's a date and set
        #   set it as the current date
        # else it's a day of week and verse, store it + current date + url-ified verse

    return


    #process each line with a bible verse to begin with it's date:
    for i in range(len(bread_lines_clean)):
        if bread_lines_clean[i][0].isdigit():
            cur_line = bread_lines_clean[i]
            cur_date = cur_line[:5] + ".2024" # e.g. 01.07.2024
            print(cur_date)
            for j in range(1, 8):
                next_line = bread_lines_clean[i + j]
                print(next_line.split(": "), "here's what we're up to")

                #string
                day_of_week, verse = next_line.split(": ")
                #return (print("pausing for now"))
                intermediary = [int(x) for x in cur_date.split(".")]
                month, day, year = intermediary[0], intermediary[1], intermediary[2] #formatting here might be off
                if day <= days_in_month[month]:
                    new_line = f"{month}.{day + j}.{year}: {verse}"
                    bread_lines_clean[i + j] = new_line
                else: #this means we're overflowing day to the next month
                    new_day = (day+j) % days_in_month[month]
                    new_line = f"{month + 1}.{new_day}.{year}: {verse}"
                    bread_lines_clean[i + j] = new_line
        i += 7


    #turn into a dictionary, add in biblegateway verse
    result_dict = {}
    for entry in bread_lines_clean:
        if entry[5:8] != "2024":
            continue 
        date, verse = entry.split(":")
        base_link = "https://www.biblegateway.com/passage/?search=" 
        verse_portions = verse.split(" ")
        link_next_half = ""
        for c in verse:
            if c == " ":
                link_next_half += "%20"
            elif c == ":":
                link_next_half += "%3A"
            else:
                link_next_half += c 
        link_next_half += "&version=NIV"

        full_link = base_link+link_next_half
        result_dict.add({date: (verse, full_link )})



    # turn it all into a CSV
    with open('verses.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
    
        # Write the header row
        writer.writerow(['Date', 'Verse', 'Link'])
    
        # Write the dictionary data row by row
        for date_d, (verse_d, link_d) in result_dict.items():
            writer.writerow([date_d, verse_d, link_d])

    return writer 


if __name__ == "__main__":
    transformText()