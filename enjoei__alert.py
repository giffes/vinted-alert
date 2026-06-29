import requests
import os
import re

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

url = "https://assets.enjoei.com.br/assets/packs/js/web/products/index-61390ecbf0f2350f332d.js"

text = requests.get(url).text

results = []

for word in ["graphql", "Search", "query", "products"]:
    for m in re.finditer(word, text, re.IGNORECASE):
        start = max(0, m.start() - 120)
        end = min(len(text), m.end() + 200)
        snippet = text[start:end]
        results.append(
            f"\n=== {word} ===\n{snippet}\n"
        )

msg = "\n".join(results[:10])

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": msg[:4000]
    }
)