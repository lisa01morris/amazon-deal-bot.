import os
import requests
import random
from PIL import Image, ImageDraw, ImageFont

# --- CONFIG ---
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]
EXNESS_LINK = "https://lisa01morris.github.io/amazon-deal-bot/"

# --- 1. SETUP ASSETS ---
def setup():
    # Download a cool background (Dark Trading Chart)
    img_data = requests.get("https://images.unsplash.com/photo-1611974765270-ca1258634369?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80").content
    with open("bg_card.jpg", "wb") as f:
        f.write(img_data)
    
    # Download a Bold Font (Roboto)
    font_data = requests.get("https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Black.ttf").content
    with open("bold.ttf", "wb") as f:
        f.write(font_data)

# --- 2. DRAW THE CARD ---
def create_card():
    asset = random.choice(["GOLD (XAU)", "BITCOIN", "GBP/USD", "US30"])
    action = random.choice(["STRONG BUY 🚀", "SELL NOW 📉"])
    price = random.randint(1900, 65000)
    
    # Open image & darken it so text pops
    img = Image.open("bg_card.jpg").convert("RGBA")
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 150)) # Black tint
    img = Image.alpha_composite(img, overlay)
    
    draw = ImageDraw.Draw(img)
    
    # Load Fonts
    font_lg = ImageFont.truetype("bold.ttf", 100)
    font_md = ImageFont.truetype("bold.ttf", 60)
    font_sm = ImageFont.truetype("bold.ttf", 40)
    
    # Draw Text (Centered)
    W, H = img.size
    
    # Title
    draw.text((W/2, 400), "⚠️ VIP SIGNAL ALERT", font=font_md, fill="#F3C623", anchor="mm")
    
    # Asset
    draw.text((W/2, 600), asset, font=font_lg, fill="white", anchor="mm")
    
    # Action (Green for Buy, Red for Sell)
    color = "#00ff00" if "BUY" in action else "#ff0000"
    draw.text((W/2, 800), action, font=font_lg, fill=color, anchor="mm")
    
    # Footer
    draw.text((W/2, 1300), "Trade with 0 Spreads", font=font_sm, fill="white", anchor="mm")
    draw.text((W/2, 1400), "LINK IN BIO", font=font_md, fill="#F3C623", anchor="mm")
    
    # Save
    img = img.convert("RGB")
    img.save("signal_card.jpg")
    return asset, action

# --- 3. SEND TO DISCORD ---
def send_discord(asset, action):
    with open("signal_card.jpg", "rb") as f:
        payload = {
            "content": f"**🚨 NEW SIGNAL CARD GENERATED!**\n\n**Strategy:** Post this to WhatsApp Status & Facebook Groups.\n**Caption:** {asset} is moving! {action} on Exness here: {EXNESS_LINK}"
        }
        requests.post(WEBHOOK_URL, data=payload, files={"file": f})

if __name__ == "__main__":
    setup()
    asset, action = create_card()
    send_discord(asset, action)
