import requests
import json
import os

URL = "https://www.vinted.pt/catalog?catalog[]=11&brand_ids[]=671&brand_ids[]=15430438&brand_ids[]=377&brand_ids[]=3573&brand_ids[]=1745&brand_ids[]=7011975&brand_ids[]=2113&brand_ids[]=14217&brand_ids[]=567&brand_ids[]=4559&brand_ids[]=83122&brand_ids[]=10613&order=newest_first&page=1"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers)
html = r.text

latest = html[:5000]

STATE_FILE = "last.txt"

old = ""
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        old = f.read()

if latest != old:

    message = "🚨 Novo item possível na sua busca Vinted!\n\n" + URL

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

    with open(STATE_FILE, "w") as f:
        f.write(latest)