import discord
from discord.ext import commands
from welcome import create_welcome_image
from AI import TTM, gbt
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

@bot.tree.command(name='embed', description=config['commands_description']['embed'])
async def poll(interaction: discord.Interaction, 
               title: str, description: str, 
               color: str, image_url: str = None, 
               foooter: str = None,
               thumbnail: str = None, onlyforme: bool = False):
                                                            
    
    global disabled
    if disabled:
        return
    
    if config["ADMIN_ID"] != interaction.user.id and onlyforme == True:
        await interaction.response.send_message(config["bot_responses"]["ephermal"], ephemeral=True)
        return
                

    embed = discord.Embed(title=title, description=description, color=getattr(discord.Color, color)())
    if image_url:
        embed.set_image(url=image_url)
    if foooter:
        embed.set_footer(text=foooter)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    

    
    if onlyforme == True:
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    await interaction.response.send_message(embed=embed, ephemeral=False)



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return


    if message.content.startswith(config["Prefix_to_AI"]):
        
        if isinstance(message.channel, discord.DMChannel):
            q = discord.Embed(description=config["bot_responses"]["no_rights"], color=0xFF4500)
            await message.channel.send(embed=q)
            return
        
        text_after_prefix = message.content[len(config["Prefix_to_AI"]):].strip()
        print(config["bot_prints"]["new_AI"], text_after_prefix)

        if config["Use_Emded_to_AI"] == "True":
            embed = discord.Embed(title=f'** Вопрос: {text_after_prefix}**', description=gbt(text_after_prefix), color=0x40E0D0)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(text_after_prefix)




@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Ошибка.")

        
@bot.event
async def on_ready():
    print(config["bot_prints"]["bot_login_print"])
    await bot.tree.sync()
    await bot.change_presence(activity=discord.CustomActivity(name=config["default_status"]))


client.run('')
