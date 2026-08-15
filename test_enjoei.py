import requests

url = "https://enjusearch.enjoei.com.br/graphql-search-x"

params = {
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

headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
}

response = requests.get(
    url,
    params=params,
    headers=headers,
    timeout=30,
)

print("STATUS:", response.status_code)
print("URL:", response.url)
print()

response.raise_for_status()

data = response.json()

products = data["data"]["search"]["products"]

print("TOTAL:", products["total"])
print("RECEIVED:", len(products["edges"]))
print()

print("PRODUCTS:")

for edge in products["edges"]:
    product = edge["node"]

    print(
        product["id"],
        "|",
        product["title"]["name"],
        "| R$",
        product["price"]["current"],
    )