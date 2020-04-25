from bs4 import BeautifulSoup
import requests
import csv
import re


# Create the file
csv_file = open("stuff.csv", mode="w")
fields = ["designation", "name"]
csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
csv_writer.writeheader()

url = "http://www.ece.upatras.gr/index.php/el/faculty.html"

html = requests.get(url).content
soup = BeautifulSoup(html, "lxml")

container = soup.find_all("div", class_="sppb-row-container")[1]
for row in container.find_all("div", class_="sppb-col-md-4"):
    for person in row.find_all("div", class_="sppb-person-information"):
        # Get the designation
        designation_wrapper = person.find("span", class_="sppb-person-designation")
        first_element_re = re.search(
            r'<span class="sppb-person-designation">(.+?)<br', str(designation_wrapper)
        )
        last_element_re = re.search(r"(<br>|<br\/>)(.+?)</span>", str(designation_wrapper))
        if first_element_re and last_element_re:
            first_element = first_element_re.group(1).strip().title()
            last_element = last_element_re.group(2).strip().title()
            designation = first_element + " " + last_element
        else:
            designation = person.find("span", class_="sppb-person-designation").text.strip()

        # Get the name
        name_wrapper = (person.find("span", class_="sppb-person-name")).a.font
        last_name_re = re.search(r">(.+?)<br/>", str(name_wrapper))
        first_name_re = re.search(r"<br/>(.+?)</font>", str(name_wrapper))
        if last_name_re and first_name_re:
            last_name = last_name_re.group(1).strip().title()
            first_name = first_name_re.group(1).strip().title()
            name = last_name + " " + first_name
        else:
            name = (person.find("span", class_="sppb-person-name")).a.text

        output = {"designation": designation, "name": name}
        csv_writer.writerow(output)


print("\n\n*** Finished Scraping ***\n\n")
