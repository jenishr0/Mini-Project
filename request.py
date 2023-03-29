import requests
from bs4 import BeautifulSoup
import lxml
# for i in range(2, 12):
url = "https://www.flipkart.com/search?q=mobiles&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_1_0_na_na_na&otracker1=AS_Query_TrendingAutoSuggest_1_0_na_na_na&as-pos=1&as-type=TRENDING&suggestionId=mobiles&requestId=3859cddd-9408-4676-bc0c-141827426f4c&page=1"
s = requests.get(url)
soup = BeautifulSoup(s.text, "lxml")

names = soup.find_all("div", class_="_4rR01T")
print(names)
# next_page = soup.find("a", class_="_1LKTO3").get("href")
# comp_page = "https://www.flipkart.com" + next_page
# print(comp_page)
