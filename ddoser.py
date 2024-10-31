import requests
import random
import time
from tqdm import tqdm

SHOP_URL = "http://localhost:8000"
ITEM_IDS = []
CART_IDS = []


def create_cart():
    response = requests.post(f"{SHOP_URL}/cart")
    cart_id = response.json().get("id")
    CART_IDS.append(cart_id)
    return cart_id


def get_cart(cart_id):
    requests.get(f"{SHOP_URL}/cart/{cart_id}")


def create_item():
    item_data = {
        "name": f"Item {random.randint(1, 100)}",
        "price": round(random.uniform(10, 100), 2),
    }
    response = requests.post(f"{SHOP_URL}/item", json=item_data)
    item_id = response.json().get("id")
    ITEM_IDS.append(item_id)


def get_item(item_id):
    requests.get(f"{SHOP_URL}/item/{item_id}")


def simulate_load():
    for _ in tqdm(range(500)):

        if random.random() > 0.5:
            action = random.choice(["create_cart", "get_cart", "create_item"])
        else:
            action = "get_item"

        if action == "create_cart":
            cart_id = create_cart()
            if random.random() > 0.5:
                get_cart(cart_id)

        elif action == "get_cart" and CART_IDS:
            get_cart(random.choice(CART_IDS))

        elif action == "create_item":
            create_item()

        elif action == "get_item" and ITEM_IDS:
            get_item(random.choice(ITEM_IDS))

        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    simulate_load()
