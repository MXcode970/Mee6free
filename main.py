import discord
from welcome import create_welcome_image
import urllib.request

client = discord.Client(intents=discord.Intents.all())

async def send_welcome_message(member):
    # Получение аватарки пользователя
    url = member.avatar.url
    
    urllib.urlretrieve(url, f"avatar_{member.display_name}")

    create_welcome_image("assets/black.jpg", f"avatar_{member.display_name}", f"{member.display_name} зашёл на сервер!",
                         f"Участник #{len(member.guild.members)}", "res.png", "assets/NotoSans-Regular.ttf")
    
    # Отправка изображения в указанный канал
    channel = discord.utils.get(member.guild.channels, name="welcome")
    if channel:
        with open("res.png", "rb") as image_file:
            picture = discord.File(image_file)
            await channel.send(file=picture)
    else:
        print("Error: Welcome channel not found.")

# Обработчик события подключения нового участника
@client.event
async def on_member_join(member):
    await send_welcome_message(member)

# Обработчик события подключения нового участника
@client.event
async def on_member_join(member):
    await send_welcome_message(member)

# Запуск бота

client.run('')
