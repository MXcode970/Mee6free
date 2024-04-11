import discord
from discord.ext import commands
from welcome import create_welcome_image
import requests 
import shutil
import os

bot = commands.Bot(command_prefix='/',intents=discord.Intents.all() )


async def send_welcome_message(member):

    url = member.avatar.url
    
    res = requests.get(url, stream = True)

    if res.status_code == 200:
        with open(f"avatar_{member.display_name}.png",'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ',f"avatar_{member.display_name}.png")
    else:
        print('Image Couldn\'t be retrieved')

    create_welcome_image("assets/black.jpg", f"avatar_{member.display_name}", f"{member.display_name} зашёл на сервер!",
                         f"Участник #{len(member.guild.members)}", "res.png", "assets/NotoSans-Regular.ttf")

    channel = discord.utils.get(member.guild.channels, name="приветствие")
    if channel:
        with open("res.png", "rb") as image_file:
            picture = discord.File(image_file)
            await channel.send(file=picture)
    else:
        print("Error: Welcome channel not found.")

    os.remove(f"avatar_{member.display_name}.png")

@bot.event
async def on_member_join(member):
    await send_welcome_message(member)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.CustomActivity(name="github.com/MXcode970/Mee6free"))

@bot.command()
async def st(ctx, *, message: str):
    #замените айдишник на айди админа
    if ctx.author.id == 728600636060467200:
        await bot.change_presence(activity=discord.Game(name=message), type=3)
        await ctx.send(f"Activity status set to '{message}'")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")




client.run('')
