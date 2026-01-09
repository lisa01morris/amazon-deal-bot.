import requests
import random
import os

# --- CONFIGURATION ---
# We use "Secrets" so your Webhook isn't public
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]
AMAZON_TAG = "hlreviews07e-21"

PRODUCTS = [
    {"name": "Apple iPad Air (5th Gen)", "price": "$499.00", "original": "$599.00", "link": "https://www.amazon.com/dp/B09V3GNLBQ", "image": "https://m.media-amazon.com/images/I/61k05HQ28lL._AC_SL1500_.jpg"},
    {"name": "SAMSUNG 49-Inch Odyssey G9", "price": "$899.99", "original": "$1,399.99", "link": "https://www.amazon.com/dp/B088HH6LW5", "image": "https://m.media-amazon.com/images/I/61SQz8S+fEL._AC_SL1000_.jpg"},
    {"name": "Beats Studio3 Wireless", "price": "$169.00", "original": "$349.95", "link": "https://www.amazon.com/dp/B07HDM3D77", "image": "https://m.media-amazon.com/images/I/51-a-rJ2B9L._AC_SL1000_.jpg"},
    {"name": "Logitech G502 HERO Mouse", "price": "$39.99", "original": "$79.99", "link": "https://www.amazon.com/dp/B07PHLCD9C", "image": "https://m.media-amazon.com/images/I/61mpMH5TzkL._AC_SL1500_.jpg"},
    {"name": "Acer Nitro 5 Laptop", "price": "$699.99", "original": "$899.99", "link": "https://www.amazon.com/dp/B092YHJGMN", "image": "https://m.media-amazon.com/images/I/81bc8mA3nKL._AC_SL1500_.jpg"}
]

def post_deal():
    item = random.choice(PRODUCTS)
    
    # Add Affiliate Tag
    link = f"{item['link']}?tag={AMAZON_TAG}" if "?" not in item['link'] else f"{item['link']}&tag={AMAZON_TAG}"

    payload = {
        "username": "Amazon Deal Sniper",
        "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Amazon_icon.svg",
        "embeds": [{
            "title": f"🔥 {item['name']}",
            "description": f"**💰 Price:** {item['price']}\n❌ ~~{item['original']}~~\n⚡ *Limited Time*",
            "url": link,
            "color": 16753920,
            "thumbnail": {"url": item['image']},
            "fields": [{"name": "👉 CLICK TO BUY", "value": f"[Check Price]({link})", "inline": True}]
        }]
    }

    try:
        requests.post(WEBHOOK_URL, json=payload)
        print(f"✅ Posted: {item['name']}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    post_deal()
