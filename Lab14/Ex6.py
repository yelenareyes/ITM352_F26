# Get mortgage rates from the Hawaii Board of REALTORS website
import requests
from bs4 import BeautifulSoup

url = "https://www.hicentral.com/hawaii-mortgage-rates.php"
print("Retrieving", url)

response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
rate_table = soup.find("table")
bank = ""

for row in rate_table.find_all("tr"):
    cells = row.find_all("td")
    if cells:
        if cells[0].find("b"):
            bank = cells[0].find("b").get_text()
            term = cells[1].get_text(strip=True)
            rate = cells[2].get_text(strip=True)
        else:
            term = cells[0].get_text(strip=True)
            rate = cells[1].get_text(strip=True)

        print(f"{bank}: {term} - {rate}%")
