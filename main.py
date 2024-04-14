import discord
from discord.ext import commands
from welcome import create_welcome_image
import requests 
import shutil
import os
import json
import string

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

bot = commands.Bot(command_prefix='/',intents=discord.Intents.all() )
disabled = False


async def send_welcome_message(member):

    url = member.avatar.url
    
    res = requests.get(url, stream = True)

    file_path = f"avatar_{member.display_name}.png"


    if res.status_code == 200:
        with open(f"avatar_{member.display_name}.png",'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print(config["bot_prints"]["avatar_downloaded"],f"avatar_{member.display_name}.png")
    else:
        print(config["bot_prints"]["avatar_download_error"])

    create_welcome_image(
        config['welcome_image_template']['background_image'], file_path,
        f"{member.display_name} {config['bot_responses']['welcome_message']}",
        f"{config['bot_responses']['member_count']}{len(member.guild.members)}", "res.png",
        config['welcome_image_template']['font_path']
    )

    channel = discord.utils.get(member.guild.channels, name=config["welcome_channel_name"])
    if channel:
        with open("res.png", "rb") as image_file:
            picture = discord.File(image_file)
            await channel.send(file=picture)
    else:
        print(config["bot_prints"]["welcome_channel_not_found"])
    try:
        os.remove(f"avatar_{member.display_name}.png")
    except Exception as e:
        print(config["bot_prints"]["avatar_deleting_error"])

@bot.event
async def on_member_join(member):
    global disabled
    if disabled == True:
        return
    await send_welcome_message(member)




@bot.tree.command(name="status", description=config['commands_description']['status'])
async def status(ctx: discord.Integration, status: str):
    global disabled
    if disabled:
        return

    if ctx.user.id == config["ADMIN_ID"]:
        if status == "standart":
            await bot.change_presence(activity=discord.CustomActivity(name=config["default_status"]))
            await ctx.response.send_message(config['bot_responses']['status_updated'])
        else:
            await bot.change_presence(activity=discord.CustomActivity(name=status))
            await ctx.response.send_message(config['bot_responses']["status_custom_updated"])
    else:
        await ctx.response.send_message(config["bot_responses"]["no_rights"], ephemeral=True)
        print(config["bot_prints"]["no_rights_print"], ctx.user.display_name)

@bot.tree.command(name="stop", description=config['commands_description']['stop'])
async def stop(ctx: discord.Integration):
    global disabled
    if ctx.user.id == config["ADMIN_ID"]:
        disabled = True
        print(config["bot_prints"]["bot_disabled_print"])
        await ctx.response.send_message(config["bot_responses"]["bot_disabled"])
        await bot.change_presence(activity=discord.CustomActivity(name=config["disabeld_status"]), status=discord.Status.idle)
    else:
        await ctx.response.send_message(config["bot_responses"]["no_rights"], ephemeral=True)


@bot.tree.command(name='poll', description=config['commands_description']['poll'])
async def poll(interaction: discord.Interaction, options: str, type: str):

    options_list = options.split(',')
    if len(options_list) < 2:
        await interaction.response.send_message(config["bot_responses"]["options_in_polls"], ephemeral=True)
        return
    
    allowed = ["horizontal", "vertical"]
    if not type in allowed:
        await interaction.response.send_message(config["bot_responses"]["type"], ephemeral=True)
        return
    
    if type == "vertical":
        sep = "\n"
    else:
        sep = "    "
        
    
    description = sep.join(f":regional_indicator_{string.ascii_lowercase[i]}: {option.strip()}" 
                            for i, option in enumerate(options_list))
    embed = discord.Embed(title="Poll", description=description, color=0x00ff00)
    await interaction.response.send_message(embed=embed, ephemeral=False)



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Ошибка.")

        
@bot.event
async def on_ready():
    print("[MEE7] Login!")
    await bot.tree.sync()
    await bot.change_presence(activity=discord.CustomActivity(name=config["default_status"]))



client.run('')
