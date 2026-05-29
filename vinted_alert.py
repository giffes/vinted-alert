import requests
import os
import json

URL = "https://www.vinted.pt/api/v2/catalog/items?page=1&per_page=20&order=newest_first&catalog_ids=11&brand_ids[]=377&brand_ids[]=567&brand_ids[]=671&brand_ids[]=1745&brand_ids[]=2113&brand_ids[]=3573&brand_ids[]=4559&brand_ids[]=10613&brand_ids[]=14217&brand_ids[]=83122&brand_ids[]=7011975&brand_ids[]=15430438&brand_ids[]=51445&brand_ids[]=56974&brand_ids[]=200474&brand_ids[]=72138"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers)

print(r.status_code)
print(r.text[:500])

data = r.json()

items = data.get("items", [])

if not items:

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": "❌ API retornou zero items."
        }
    )

else:

    first = items[0]

    title = first.get("title", "Sem título")
    price = first.get("price", {}).get("amount", "?")
    url = first.get("url", "")

    msg = f"""🚨 TESTE VINTED API

{title}

€{price}

https://www.vinted.pt{url}
"""

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )