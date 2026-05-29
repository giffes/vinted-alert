import requests
import os
import re

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.vinted.pt/catalog?catalog[]=11&brand_ids[]=377&brand_ids[]=567&brand_ids[]=671&brand_ids[]=1745&brand_ids[]=2113&brand_ids[]=3573&brand_ids[]=4559&brand_ids[]=10613&brand_ids[]=14217&brand_ids[]=83122&brand_ids[]=7011975&brand_ids[]=15430438&brand_ids[]=51445&brand_ids[]=56974&brand_ids[]=200474&brand_ids[]=72138&order=newest_first&currency=EUR&page=1"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers)
html = r.text

matches = re.findall(r'\/items\/([^\"]+)', html)

items = list(dict.fromkeys(matches))

LATEST = items[0] if items else None

LAST_FILE = "last_item.txt"

previous = None

if os.path.exists(LAST_FILE):
    with open(LAST_FILE, "r") as f:
        previous = f.read().strip()

if LATEST and LATEST != previous:

    msg = f"""🚨 NOVO ITEM — Vinted

https://www.vinted.pt/items/{LATEST}
"""

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

with open(LAST_FILE, "w") as f:
    f.write(LATEST or "")