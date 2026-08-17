limport json
import os
import time
import uuid
import requests
from datetime import datetime, timezone, timedelta

URL = "https://enjusearch.enjoei.com.br/graphql-search-x"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

SEEN_FILE = "enjoei_test_seen.json"
BROWSER_ID_FILE = "enjoei_browser_id.txt"

# Termo de busca (ajuste aqui ou transforme em env var depois)
TERM = "dior"

# Fuso de Brasília (-03:00), sem depender de zoneinfo do sistema
BR_TZ = timezone(timedelta(hours=-3))


def epoch_millis():
    return int(time.time() * 1000)


def tagged_id():
    """Gera um id no MESMO formato usado pelo site: uuid4 + '-' + epoch em ms."""
    return f"{uuid.uuid4()}-{epoch_millis()}"


def get_browser_id():
    """Um navegador real reusa o mesmo browser_id entre visitas.
    Persistimos no repo pra parecer o mesmo 'visitante' a cada execução."""
    if os.path.exists(BROWSER_ID_FILE):
        with open(BROWSER_ID_FILE, "r", encoding="utf-8") as f:
            saved = f.read().strip()
            if saved:
                return saved
    new_id = tagged_id()
    with open(BROWSER_ID_FILE, "w", encoding="utf-8") as f:
        f.write(new_id)
    return new_id


def build_params():
    now = datetime.now(BR_TZ).strftime("%Y-%m-%dT%H:%M:%S-03:00")
    return {
        "browser_id": get_browser_id(),
        "city": "rio-de-janeiro",
        "experienced_seller": "true",
        "first": "20",
        "last_published_at": now,
        "operation_name": "searchProducts",
        "query_id": "c5faa5f85fb47bf0beaa97b67d8a9189",
        "search_context": "products_search",
        "search_id": tagged_id(),
        "shipping_range": "same_country",
        "state": "rj",
        "term": TERM,
    }


HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
}


def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))


def save_seen(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f)


def send_telegram(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "disable_web_page_preview": False,
        },
        timeout=30,
    )


def main():
    params = build_params()
    response = requests.get(URL, params=params, headers=HEADERS, timeout=30)
    print("STATUS:", response.status_code)

    if response.status_code != 200:
        send_telegram(
            f"⚠️ Enjoei test falhou.\nSTATUS: {response.status_code}\n"
            f"BODY: {response.text[:500]}"
        )
        response.raise_for_status()

    data = response.json()

    if "errors" in data:
        send_telegram(f"⚠️ Enjoei API retornou erro:\n{json.dumps(data['errors'])[:800]}")
        return

    products = data["data"]["search"]["products"]
    edges = products["edges"]
    total = products["total"]

    seen = load_seen()
    is_first_run = len(seen) == 0

    new_products = []
    for edge in edges:
        node = edge["node"]
        if node["id"] not in seen:
            new_products.append(node)

    print("TOTAL:", total)
    print("RECEIVED:", len(edges))
    print("SEEN (antes):", len(seen))
    print("NEW:", len(new_products))

    # Se a API não devolveu nenhum produto, algo está bloqueando/errado.
    # Avisa e NÃO salva estado vazio, pra não ficar preso em "bootstrap" pra sempre.
    if len(edges) == 0:
        send_telegram(
            "⚠️ Enjoei test: a API respondeu 200 mas veio sem produtos.\n"
            f"TOTAL relatado: {total}\n"
            f"browser_id: {params['browser_id']}\n"
            f"search_id: {params['search_id']}\n"
            f"last_published_at: {params['last_published_at']}\n"
            "Possível bloqueio anti-bot ou parâmetro inválido."
        )
        return

    # Bootstrap: na primeira execução só salva o estado, não manda spam
    if is_first_run:
        for edge in edges:
            seen.add(edge["node"]["id"])
        save_seen(seen)
        send_telegram(
            f"✅ Enjoei test bootstrap concluído.\nTOTAL: {total}\nItens salvos: {len(seen)}"
        )
        print("Bootstrap completed.")
        return

    for product in new_products:
        name = product["title"]["name"]
        price = product["price"]["current"]
        path = product["path"]
        product_url = f"https://www.enjoei.com.br/p/{path}"

        msg = f"🆕 NOVO ENJOEI\n\n{name}\nR$ {price}\n\n{product_url}"
        send_telegram(msg)

    for edge in edges:
        seen.add(edge["node"]["id"])
    save_seen(seen)

    print(f"Enviados ao Telegram: {len(new_products)}")


if __name__ == "__main__":
    main()
