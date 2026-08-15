import json
import os
import requests

URL = "https://enjusearch.enjoei.com.br/graphql-search-x"

PARAMS = {
    "browser_id": "62f8d758-0023-431b-9fe8-dc9a021c1c1c-1786824839265",
    "city": "rio-de-janeiro",
    "experienced_seller": "true",
    "first": "20",
    "last_published_at": "2026-08-14T17:18:30-03:00",
    "operation_name": "searchProducts",
    "query_id": "c5faa5f85fb47bf0beaa97b67d8a9189",
    "search_context": "products_search",
    "search_id": "d1ab9ddb-67a4-407f-8233-3c269f02bd6e-1786824848579",
    "shipping_range": "same_country",
    "state": "rj",
    "term": "dior",
}

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
}

SEEN_FILE = "enjoei_test_seen.json"


def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()

    with open(SEEN_FILE, "r", encoding="utf-8") as file:
        return set(json.load(file))


def save_seen(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as file:
        json.dump(list(seen), file)


response = requests.get(
    URL,
    params=PARAMS,
    headers=HEADERS,
    timeout=30,
)

print("STATUS:", response.status_code)

response.raise_for_status()

data = response.json()

products = data["data"]["search"]["products"]
edges = products["edges"]

seen = load_seen()

new_products = []

for edge in edges:
    product = edge["node"]

    product_id = product["id"]

    if product_id not in seen:
        new_products.append(product)

print()
print("TOTAL:", products["total"])
print("RECEIVED:", len(edges))
print("SEEN:", len(seen))
print("NEW:", len(new_products))
print()

print("NEW PRODUCTS:")

for product in new_products:
    print(
        product["id"],
        "|",
        product["title"]["name"],
        "| R$",
        product["price"]["current"],
    )

# Salva todos os produtos atuais como vistos
for edge in edges:
    seen.add(edge["node"]["id"])

save_seen(seen)