import requests
import os
import re

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.enjoei.com.br/dior/s?ref=products_search&sid=c4a381b4-775e-4deb-a3ff-f8868b4bf0f2-1782692777976&q=dior&lp=24h&sr=same_country"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers)

html = r.text

checks = {
    "product": html.lower().count("product"),
    "offer": html.lower().count("offer"),
    "price": html.lower().count("price"),
    "graphql": html.lower().count("graphql"),
    "__next": html.lower().count("__next"),
    "itemprop": html.lower().count("itemprop"),
}

msg = f"""
ENJOEI CHECK

status: {r.status_code}

{checks}

graphql positions:
{html.lower().find('graphql')}

__next positions:
{html.lower().find('__next')}

itemprop positions:
{html.lower().find('itemprop')}
"""

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": msg
    }
)