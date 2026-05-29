import requests
import os
import re
import json
from datetime import datetime

print("RUN:", datetime.utcnow())

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.vinted.pt/catalog?catalog[]=11&brand_ids[]=377&brand_ids[]=567&brand_ids[]=671&brand_ids[]=1745&brand_ids[]=2113&brand_ids[]=3573&brand_ids[]=4559&brand_ids[]=10613&brand_ids[]=14217&brand_ids[]=83122&brand_ids[]=7011975&brand_ids[]=15430438&brand_ids[]=51445&brand_ids[]=56974&brand_ids[]=200474&brand_ids[]=72138&order=newest_first&currency=EUR&page=1"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers)

html = r.text

matches = re.findall(r'/items/([0-9]+)-', html)

current_ids = list(dict.fromkeys(matches))[:50]

STATE_FILE = "seen.json"

if os.path.exists(STATE_FILE):

    with open(STATE_FILE, "r") as f:
        previous_ids = json.load(f)

else:

    previous_ids = []

# bootstrap → primeira execução não manda spam
if not previous_ids:

    with open(STATE_FILE, "w") as f:
        json.dump(current_ids, f)

    print("Bootstrap completed.")
    exit()

new_ids = [x for x in current_ids if x not in previous_ids]

for item_id in reversed(new_ids):

    msg = f"""🚨 NOVO ITEM — Vinted

https://www.vinted.pt/items/{item_id}
"""

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

with open(STATE_FILE, "w") as f:
    json.dump(current_ids, f)

print(f"New items: {len(new_ids)}")