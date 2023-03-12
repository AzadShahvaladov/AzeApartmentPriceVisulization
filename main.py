import requests
from bs4 import BeautifulSoup
import pandas as pd
from data_prepearing import DataPrepear

page = 1
price_list = []
location_list = []
rooms_list = []
square_list = []
floor_list = []

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.141 Mobile Safari/537.36"
}

while True:
    print(str(page) + ' page scanned')
    url, page = 'https://bina.az/alqi-satqi/menziller?page=' + str(page), page + 1
    req = requests.get(url, headers)

    html_page = req.text

    if "items items--no-results" in html_page:
        break

    soup = BeautifulSoup(html_page, "lxml")
    all_adds_href = soup.select("div[class=items_list]")
    price = all_adds_href[0].find_all(class_="price-val")
    location = all_adds_href[0].find_all(class_="location")
    name = all_adds_href[0].find_all(class_="name")

    for item in price:
        price_number = item.text.replace(" ", "")
        price_list.append(int(price_number))

    for item in location:
        location_list.append(item.text)

    for item in name:

        name = item.find_all("li")
        rooms_number = name[0].text.split()[0]
        square_number = name[1].text.split()[0]
        rooms_list.append(int(rooms_number))
        square_list.append(float(square_number))
        try:
            floor_number = name[2].text.split()[0]
            floor_list.append(floor_number)
        except IndexError:
            floor_list.append(0)
            print('Append 0 to list')


data_dict = {
        "price": price_list,
        "location": location_list,
        "rooms": rooms_list,
        "square": square_list,
        "floor": floor_list
        }

df = pd.DataFrame(data_dict)

df.to_csv("binatable.csv")

df = pd.read_csv("binatable.csv")

df_visualization_prepared = DataPrepear(df)

df.rename(str.lower, axis='columns', inplace=True)
df.rename(columns={"shape": "square", "shape_range": "square_range"}, inplace=True)
df.to_csv("binaaz.csv", index=False)
