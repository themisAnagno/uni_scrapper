from bs4 import BeautifulSoup
import requests
import csv

# Base url
url = "http://www.ece.upatras.gr/index.php/el/proptixiaka-an.html"

# Open the csv file
csv_file = open("announments.csv", mode="w")
fields = ["date", "announcement", "link"]
csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
csv_writer.writeheader()

while True:
    html = requests.get(url).content

    # Find the host url
    host = url.split("/index")[0]

    # Create the soup of the html site
    soup = BeautifulSoup(html)

    # Get the table of announcements
    announcement_table = soup.find(
        "table", class_="category table table-striped table-bordered table-hover"
    )

    # Get the rows of the announcement table in a list
    announc_rows = announcement_table.tbody.find_all("tr")

    for entry in announc_rows:
        data = entry.find_all("td")
        announcement = data[0].a.text.strip()
        link = host + data[0].a["href"]
        date = data[1].text.strip()

        output = {"date": date, "announcement": announcement, "link": link}
        csv_writer.writerow(output)

    pagination = soup.find("div", class_="pagination")
    try:
        next_link = pagination.find("a", title="Επόμενο")["href"]
    except TypeError:
        break
    else:
        next_page = host + next_link
        url = next_page

csv_file.close()

print("CSV File with all the announcements has been created")
