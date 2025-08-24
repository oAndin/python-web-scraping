# url = ("https://www.paguemenos.com.br/inalador-nebulizador-pague-menos-portatil-ultrassonico-mesh-nb1100/p?skuId=100141&srsltid=AfmBOoqwD9v54eYWCbhMpUEnaSxrWk4BaWeWr0BGIhmNLysout0mVbdM5mI");
#
# response = requests.get(url);
#
# html_content = response.text;
#
# soup = BeautifulSoup(html_content, "lxml")
#"
# # Get all text
# text = soup.get_text(" ", strip=True)
#
# # Regex: find "ean" followed by 8-14 digits
# pattern = re.compile(r"ean[^\d]*(\d{8,14})", re.IGNORECASE)
# matches = pattern.findall(text)
#
# if matches:
#     for match in matches:
#         print("Found EAN:", match)
# else:
#     print("No EAN found in static HTML")

import requests
from bs4 import BeautifulSoup
import re
url = "https://www.paguemenos.com.br/inalador-nebulizador-pague-menos-portatil-ultrassonico-mesh-nb1100/p?skuId=100141&srsltid=AfmBOoqwD9v54eYWCbhMpUEnaSxrWk4BaWeWr0BGIhmNLysout0mVbdM5mI"

response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

# Get all text
text = soup.get_text(" ", strip=True)

# Regex: find "ean" followed by 8-14 digits
pattern = re.compile(r"ean", re.IGNORECASE);
matches = pattern.findall(text);

# print(soup)

if matches:
    for match in matches:
        print("Found EAN:", match)
else:
    print("No EAN found in static HTML")