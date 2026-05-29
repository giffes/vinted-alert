import requests
import os
import re

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.vinted.pt/catalog?catalog[]=11&brand_ids[]=377&brand_ids[]=567&brand_ids[]=671&brand_ids[]=1745&brand_ids[]=2113&brand_ids[]=3573&brand_ids[]=4559&brand_ids[]=10613&brand_ids[]=14217&brand_ids[]=83122&brand_ids[]=7011975&brand_ids[]=15430438&brand_ids[]=51445&brand_ids[]=56974&brand_ids[]=200474&brand_ids[]=72138&order=newest_first&currency=EUR&page=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136 Safari/537.36"
}

r = requests.get(URL, headers=headers)

html = r.text

titles = re.findall(r'"title":"([^"]+)"', html)

prices = re.findall(r'"price":"([^"]+)"', html)

links = re.findall(r'"/items/([^"]+)"', html)

msg = f"""
DEBUG

titles encontrados: {len(titles)}
prices encontrados: {len(prices)}
links encontrados: {len(links)}

primeiro título:

{titles[0] if titles else "NONE"}

primeiro preço:

{prices[0] if prices else "NONE"}

primeiro link:

{links[0] if links else "NONE"}
"""

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": msg[:4000]
    }
)