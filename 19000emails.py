import requests
from bs4 import BeautifulSoup
import time
import random
import json
from fake_useragent import UserAgent

ua = UserAgent()
info = []
count = 0
errors_count = 0

for i in range(1, 636):
    headers1 = {
        "Accept": "*/*",
        "user-agent": ua.random
    }
    url = f'https://www.wlw.de/de/suche/page/{i}?q=maschinenbau'  # link to site
    q = requests.get(url=url, headers=headers1)
    result = q.content
    soup = BeautifulSoup(result, 'lxml')
    hrefs = soup.find_all(class_="company-title-link")
    for h in hrefs:
        headers2 = {
            "Accept": "*/*",
            "user-agent": ua.random
        }
        time.sleep(random.uniform(0.05, 0.08))
        link = "https://www.wlw.de" + h.get("href")
        req = requests.get(url=link, headers=headers2)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        try:
            email = soup.find(id="location-and-contact__email").text
            email = email.replace(email[0:6], "")
            name = soup.find(class_="direct-contact__person").text.replace("\n", "").replace("    ", "").replace("   ",
                                                                                                                 " ").replace(
                "  ", " ").replace("     ", " ").replace("ö", "o").replace("Ü", "u").replace("ä", "a")
        except Exception:
            count += 1
            print("ERORR")
            continue
        info.append(
            {
                "email": email,
                "name": name
            })
        with open("data/19000.json", "w", encoding="utf-8") as file:
            json.dump(info, file, indent=4, ensure_ascii=False)
        count += 1
        print(str(count) + f"/19000")
