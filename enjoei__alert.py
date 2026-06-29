import requests
import os
import re

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

url = "https://assets.enjoei.com.br/assets/packs/js/web/products/index-61390ecbf0f2350f332d.js"

text = requests.get(url).text

matches = re.findall(
    r'graphql|operationName|query|search|products',
    text,
    re.IGNORECASE
)

msg = f"""
JS SIZE: {len(text)}

MATCHES:
{matches[:50]}
"""

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": msg[:4000]
    }
)