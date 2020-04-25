from bs4 import BeautifulSoup
import requests
import csv
import re


# Create the file
csv_file = open("stuff.csv", mode="w")
fields = ["designation", "name", "division", "courses"]
csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
csv_writer.writeheader()

host = "http://www.ece.upatras.gr"
url = host + "/index.php/el/faculty.html"

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

        # Get the link
        person_link = host + person.find("span", class_="sppb-person-name").a["href"]

        person_html = requests.get(person_link).content
        person_soup = BeautifulSoup(person_html, "lxml")

        # Get the division
        division = person_soup.find("span", class_="sppb-person-email").a.text

        # Get the teaching link
        teaching_link = (
            person_link
            + person_soup.find("ul", class_="sppb-nav sppb-nav-pills").find_all("li")[1].a["href"]
        )
        try:
            teaching_html = requests.get(teaching_link).content
            teaching_soup = BeautifulSoup(teaching_html, "lxml")

            # Get the courses table
            courses_text = (
                teaching_soup.find_all("div", class_="sppb-addon sppb-addon-text-block 0")[1]
                .find("div", class_="sppb-addon-content")
                .text.strip()
            )
            courses = re.sub(r"(\n)+", "\n", courses_text).replace("\xa0", " ")
        except AttributeError:
            print(f"Could not parse for {name}")
            courses = "N/A"

        output = {
            "designation": designation,
            "name": name,
            "division": division,
            "courses": courses,
        }
        csv_writer.writerow(output)

csv_file.close()
print("\n\n*** Finished Scraping ***\n\n")
