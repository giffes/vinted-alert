import requests
import os
import re
import json

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

STATE_FILE = "seen.json"

seen = []

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        seen = json.load(f)

new_seen = items[:20]

for item in items[:20]:

    if item not in seen:

        msg = f"""🚨 NOVO ITEM — Vinted

https://www.vinted.pt/items/{item}
"""

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": msg
            }
        )

with open(STATE_FILE, "w") as f:
    json.dump(new_seen, f)