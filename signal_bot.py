import google.generativeai as genai
import requests
import os
import random

# --- CONFIGURATION ---
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]
EXNESS_LINK = "https://lisa01morris.github.io/amazon-deal-bot/" # Your Bridge Page Link

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Assets to rotate through
ASSETS = ["Gold (XAUUSD)", "Bitcoin (BTC)", "EURUSD", "NASDAQ (US100)", "Tesla"]

def send_discord_message(content):
    payload = {
        "username": "AI Trading Signals",
        "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Infographics_Financial_charts_and_graphs.jpg/640px-Infographics_Financial_charts_and_graphs.jpg",
        "embeds": [{
            "title": "🧠 New AI Viral Content Generated",
            "description": content,
            "color": 5814783, # Blue
            "footer": {"text": "Copy and Post this to TikTok/Twitter/Reddit!"}
        }]
    }
    requests.post(WEBHOOK_URL, json=payload)

def generate_signal():
    asset = random.choice(ASSETS)
    print(f"Analyzing {asset}...")
    
    prompt = f"""
    You are a viral content strategist for a Forex Trader.
    Write 3 SOCIAL MEDIA POSTS about {asset} moving in the market today.
    Assume the trend is volatile/interesting.
    
    OUTPUT FORMAT:
    
    **1. TWEET (Twitter/X):**
    (Short, punchy, use 🚀, under 280 chars)
    
    **2. REDDIT TITLE & BODY:**
    (Professional analysis, bullet points, convincing tone)
    
    **3. TIKTOK SCRIPT:**
    (Hook: "Stop scrolling!", Body: "Here is why {asset} is exploding...", CTA: "Link in Bio to trade with 0 spreads")
    
    **LINK TO USE:** {EXNESS_LINK}
    """
    
    try:
        response = model.generate_content(prompt)
        text_output = response.text
        
        # Send to Discord
        send_discord_message(text_output)
        print("✅ Signal sent to Discord!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    generate_signal()
