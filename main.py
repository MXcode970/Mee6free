import discord
from discord.ext import commands
from welcome import create_welcome_image
import requests 
import shutil
import os

bot = commands.Bot(command_prefix='/',intents=discord.Intents.all() )
disabled = False


async def send_welcome_message(member):

    url = member.avatar.url
    
    res = requests.get(url, stream = True)

    if res.status_code == 200:
        with open(f"avatar_{member.display_name}.png",'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('[MEE7] Avatar sucessfully Downloaded: ',f"avatar_{member.display_name}.png")
    else:
        print('[MEE7] [ERROR] Image Couldn\'t be retrieved')

    create_welcome_image("assets/black.jpg", f"avatar_{member.display_name}", f"{member.display_name} зашёл на сервер!",
                         f"Участник #{len(member.guild.members)}", "res.png", "assets/NotoSans-Regular.ttf")

    channel = discord.utils.get(member.guild.channels, name="приветствие")
    if channel:
        with open("res.png", "rb") as image_file:
            picture = discord.File(image_file)
            await channel.send(file=picture)
    else:
        print("[MEE7] [ERROR] Welcome channel not found.")
    try:
        os.remove(f"avatar_{member.display_name}.png")
    except Exception as e:
        print(f"[MEE7] [ERROR] I cant delete avatar_{member.display_name}.png")

@bot.event
async def on_member_join(member):
    global disabled
    if disabled == True:
        return
    await send_welcome_message(member)




@bot.tree.command(name="status", description="Поставить статус")
async def status(ctx: discord.Integration, status: str):
    global disabled
    if disabled:
        return

    if ctx.author.id == 728600636060467200:
        await bot.change_presence(activity=discord.CustomActivity(name=status))
        await ctx.response.send_message(f"Updated. **'{status}'**")
    else:
        print(f"[MEE7] {ctx.author.display_name} No rights")

@bot.command()
async def disablemee7(ctx):
    global disabled
    if ctx.author.id == 728600636060467200:
        disabled = True
        print("[MEE7] Disabled")
        await bot.change_presence(activity=discord.CustomActivity(name="Disabled"), status=discord.Status.idle)

        
@bot.event
async def on_ready():
    print("[MEE7] Login!")
    await bot.tree.sync()
    await bot.change_presence(activity=discord.CustomActivity(name="github.com/MXcode970/Mee6free"))


client.run('')
