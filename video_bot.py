import os
import asyncio
import random
import requests
import google.generativeai as genai
import edge_tts
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip

# --- CONFIG ---
GEMINI_KEY = os.environ["GEMINI_KEY"]
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]
EXNESS_LINK = "https://lisa01morris.github.io/amazon-deal-bot/"

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- 1. GET THE SCRIPT ---
def get_script():
    asset = random.choice(["Bitcoin", "Gold", "USD/JPY", "Tesla"])
    prompt = f"""
    Write a SHORT 3-sentence script for a TikTok video about {asset} moving fast.
    Do NOT include visual instructions. Just the spoken words.
    Ending: "Link in bio to trade with zero spreads."
    """
    response = model.generate_content(prompt)
    return response.text.replace("*", "").strip()

# --- 2. GENERATE AUDIO ---
async def generate_audio(text):
    voice = "en-US-ChristopherNeural" # Male forceful voice
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")

# --- 3. MAKE VIDEO ---
def make_video(script_text):
    # Background: Download a static chart image
    img_url = "https://images.unsplash.com/photo-1611974765270-ca1258634369?ixlib=rb-4.0.3&auto=format&fit=crop&w=1080&q=80"
    img_data = requests.get(img_url).content
    with open("bg.jpg", "wb") as handler:
        handler.write(img_data)

    # Audio
    audio = AudioFileClip("voice.mp3")
    duration = audio.duration + 1

    # Visuals
    clip = ImageClip("bg.jpg").set_duration(duration)
    clip = clip.resize(height=1920) # Make it vertical
    clip = clip.crop(x1=0, y1=0, width=1080, height=1920)

    # Text Overlay
    # Note: TextClip requires ImageMagick, which is hard on GitHub. 
    # We will skip complex text and just make a video with audio + background.
    
    final_clip = clip.set_audio(audio)
    final_clip.write_videofile("final_video.mp4", fps=24)

# --- 4. SEND TO DISCORD ---
def send_to_discord(script_text):
    with open("final_video.mp4", "rb") as f:
        payload = {"content": f"🚀 **New AI Video Ready!**\nScript: {script_text}\n\n**DOWNLOAD AND POST TO TIKTOK/REELS 👇**"}
        requests.post(WEBHOOK_URL, data=payload, files={"file": f})

# --- RUN ---
if __name__ == "__main__":
    script = get_script()
    print(f"Script: {script}")
    asyncio.run(generate_audio(script))
    make_video(script)
    send_to_discord(script)
