import discord
from welcome import create_welcome_image
import requests 
import shutil

client = discord.Client(intents=discord.Intents.all())

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


@client.event
async def on_member_join(member):
    await send_welcome_message(member)


@client.event
async def on_member_join(member):
    await send_welcome_message(member)



client.run('')
