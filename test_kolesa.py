import requests
from bs4 import BeautifulSoup
import csv

CSV = "cars.csv"
HOST = "https://kolesa.kz"
URL = "https://kolesa.kz/cars/avtomobili-s-probegom/toyota/camry/"
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
}

def get_html(url, params=""):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items_white = soup.find_all("div", class_="row vw-item list-item a-elem")
    items_yellow = soup.find_all("div", class_="row vw-item list-item yellow a-elem")
    items_blue = soup.find_all("div", class_="row vw-item list-item blue a-elem")
    items = items_blue + items_yellow + items_white
    cars = []


    for item in items:
        cars.append(
            {
                "title": item.find("span", class_="a-el-info-title").get_text(strip=True),#.split("_"),
                "link_car": HOST + item.find("a", class_="list-link").get("href"),
                "price": item.find("span", class_="price").get_text(strip=True).replace("&nbsp;", " ").replace("\xa0"," "),
                "city": item.find("div", class_="list-region").get_text(strip=True),
                "date": item.find("span", class_="date").get_text(strip=True),
                # "view": item.find("span", class_="nb-views-int").get_text(strip=True),
                # "description": item.find("div", class_="a-search-description").get_text(strip=True),
            }
        )

    return cars

def save_csv(items, path):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file, delimiter=" ")
        # writer.writerow([["model"], ["link"], ["описание"], ["price"], ["город"], ["дата"]])
        for item in items:
            writer.writerow([item["title"], item["price"], item["city"], item["date"], item["link_car"]])

# item["description"], item["view"]

def parser():
    PAGENATION = input("введите стр: ")
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        for page in range(1, PAGENATION):
            print(f"parsing page: {page}")
            html = get_html(URL, params={"page": page})
            cars.extend(get_content(html.text))
            save_csv(cars, CSV)
    else:
        print("Error")

parser()






