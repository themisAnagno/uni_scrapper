from bs4 import BeautifulSoup
import requests
import csv

# Create the csv output file
csv_file = open("di.announc.csv", mode="w")
fields = ["date", "title", "link"]
csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
csv_writer.writeheader()

# Base url
host = "http://www.di.uoa.gr"
url = host

page = 0
while True:
    page += 1
    # Get the HTML page
    html = requests.get(url).content

    # Create the soup from the html page
    soup = BeautifulSoup(html, "lxml")

    # Get the announcement panel
    news_panel = soup.find("div", class_="panel-pane pane-views pane-news")

    # Get the news container
    news_container = news_panel.find("div", class_="view-content")

    news_list = news_container.find_all("div", class_="views-row")

    for item in news_list:
        date = item.find("div", class_="views-field-created").span.text
        title = item.find("div", class_="views-field-title").a.text
        link = host + item.find("div", class_="views-field-title").a["href"]

        output = {"date": date, "title": title, "link": link}
        csv_writer.writerow(output)

    pagination = news_panel.find("div", class_="item-list")
    try:
        next_page = pagination.find("li", class_="pager-next").a["href"]
    except TypeError:
        break
    else:
        url = host + next_page

csv_file.close()
print("\n\n*** Finished scrapping di.uoa announcements ***\n\n")
