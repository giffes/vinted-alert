import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

url = "https://enjusearch.enjoei.com.br/graphql"

r = requests.get(url)

msg = f"""
STATUS: {r.status_code}

HEADERS:

{dict(r.headers)}

BODY:

{r.text[:1000]}
"""

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": msg[:4000]
    }
)