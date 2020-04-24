from bs4 import BeautifulSoup
import requests
import csv


# Create the file
csv_file = open("stuff.csv", mode="w")
fields = ["designation", "name"]
csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
csv_writer.writeheader()

url = "http://www.ece.upatras.gr/index.php/el/faculty.html"

html = requests.get(url).content
soup = BeautifulSoup(html)

container = soup.find_all("div", class_="sppb-row-container")[1]
for row in container.find_all("div", class_="sppb-col-md-4"):
    for person in row.find_all("div", class_="sppb-person-information"):
        designation = person.find("span", class_="sppb-person-designation").text
        name = (person.find("span", class_="sppb-person-name")).a.text

        output = {"designation": designation, "name": name}
        csv_writer.writerow(output)


print("\n\n*** Finished Scraping ***\n\n")
