import os
import asyncio
import random
import requests
import google.generativeai as genai
import edge_tts
from moviepy.editor import ImageClip, AudioFileClip

# --- CONFIG ---
GEMINI_KEY = os.environ["GEMINI_KEY"]
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]
# YOUR SAFE LINK IS HERE:
EXNESS_LINK = "https://lisa01morris.github.io/amazon-deal-bot/"

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- 1. GET THE SCRIPT ---
def get_script():
    asset = random.choice(["Bitcoin", "Gold", "USD/JPY", "Tesla", "XRP"])
    prompt = f"""
    Write a SHORT 2-sentence hook for a TikTok video about {asset}.
    It must sound urgent and wealthy.
    Do NOT include visual instructions. Just the spoken words.
    """
    response = model.generate_content(prompt)
    return response.text.replace("*", "").strip()

# --- 2. GENERATE AUDIO ---
async def generate_audio(text):
    # Using a fast, deep male voice
    voice = "en-US-ChristopherNeural" 
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")

# --- 3. MAKE VIDEO ---
def make_video():
    # Background: High-quality trading chart
    img_url = "https://images.unsplash.com/photo-1611974765270-ca1258634369?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80"
    img_data = requests.get(img_url).content
    with open("bg.jpg", "wb") as handler:
        handler.write(img_data)

    # Audio
    audio = AudioFileClip("voice.mp3")
    duration = audio.duration + 0.5

    # Visuals
    clip = ImageClip("bg.jpg").set_duration(duration)
    # Resize to vertical phone screen (9:16 aspect ratio)
    clip = clip.resize(height=1920)
    clip = clip.crop(x1=0, y1=0, width=1080, height=1920)
    
    final_clip = clip.set_audio(audio)
    final_clip.write_videofile("final_video.mp4", fps=24)

# --- 4. SEND TO DISCORD (AUTO-LINK FIXED) ---
def send_to_discord(script_text):
    # This prepares the exact text you need to paste
    caption_to_copy = f"🔥 {script_text}\n\n👇 START TRADING HERE:\n{EXNESS_LINK}"
    
    with open("final_video.mp4", "rb") as f:
        payload = {
            "content": f"**✅ VIDEO READY!**\n\n1. Save the video below.\n2. **COPY** the text in the box below for your caption:\n```\n{caption_to_copy}\n```",
        }
        requests.post(WEBHOOK_URL, data=payload, files={"file": f})

# --- RUN ---
if __name__ == "__main__":
    print("Generating Script...")
    script = get_script()
    
    print("Generating Audio...")
    asyncio.run(generate_audio(script))
    
    print("Rendering Video...")
    make_video()
    
    print("Sending to Discord...")
    send_to_discord(script)
