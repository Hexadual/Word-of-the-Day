from PIL import Image # Used for image manipulation
from PIL import ImageFont
from PIL import ImageDraw
from discord.ext import tasks # Used for scheduling
from dotenv import load_dotenv
import os # Used for .env
import datetime # Used to compare time
import random # Used for selecting random word
import discord # Used for bot

load_dotenv(".env")

TOKEN = os.getenv("DISCORD_TOKEN") 
BOT = discord.Client()
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

with open("words.txt", "r") as wordsfile: # Get our words into a list (4500+ words!)
	words = wordsfile.read()
	wordslist = words.split(",")

def generate_image(): # Optimize this
	image = Image.open("nixon.png")
	font = ImageFont.truetype("impact",72)
	draw = ImageDraw.Draw(image)
	##########################################
	
	textsize = font.getsize("RICHARD NIXON")
	draw.text(((image.size[0]-textsize[0])/2, 0), "RICHARD NIXON", font=font, fill=(255,255,255), stroke_width=3, stroke_fill=(0,0,0))
	textsize = font.getsize("WORD OF THE DAY")
	draw.text(((image.size[0]-textsize[0])/2, textsize[1]), "WORD OF THE DAY", font=font, fill=(255,255,255), stroke_width=3, stroke_fill=(0,0,0))
	randomword = wordslist[random.randint(0,len(wordslist))].upper()
	textsize = font.getsize(randomword)
	draw.text(((image.size[0]-textsize[0])/2, image.size[1]-textsize[1]-(textsize[1]/8)), randomword, font=font, fill=(255,255,255), stroke_width=3, stroke_fill=(0,0,0))
	image = image.resize((image.size[0]//6,image.size[1]//6))
	image.save("sample-out.png")
	return randomword

async def send_message():
	word = generate_image()
	channel = BOT.get_channel(CHANNEL_ID)
	await channel.send(file=discord.File("sample-out.png"))
	await BOT.change_presence(activity=discord.Activity(name=f"word of the day: {word}", type=discord.ActivityType.watching))

@tasks.loop(seconds=1)
async def check_time(): # Runs every second and checks the time.
	now = datetime.datetime.now()
	if now.hour == 7 and now.minute == 0 and now.second == 0:
		print("Sending message...")
		await send_message()
		print("Sent message.")

@check_time.before_loop # Wait for the bot to be ready before we start the loop
async def before_bot():
	await BOT.wait_until_ready()

@BOT.event # Bot turns on
async def on_ready():
    print(f"Logged in as {BOT.user.name}")
    print(f"Outputting to #{BOT.get_channel(CHANNEL_ID)}")
    await BOT.change_presence(activity=discord.Activity(name=f"word of the day: NONE", type=discord.ActivityType.watching))

if __name__ == "__main__":
	check_time.start()
	BOT.run(TOKEN)