import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.enjoei.com.br/dior/s?ref=products_search&sid=c4a381b4-775e-4deb-a3ff-f8868b4bf0f2-1782692777976&q=dior&lp=24h&sr=same_country"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers)

html = r.text

msg = f"""ENJOEI HTML

status: {r.status_code}

first 2000 chars:

{html[:2000]}
"""

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": msg[:4000]
    }
)