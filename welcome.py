from PIL import Image, ImageDraw, ImageFont

def create_welcome_image(background_path, profile_image_path, top_text, bottom_text, output_path, font_path):

    background = Image.open(background_path).convert("RGBA")
    bg_width, bg_height = background.size
    background = background.resize((round(bg_width * 0.8), round(bg_height * 0.8)))


    profile_image = Image.open(profile_image_path).convert("RGBA")
    profile_image = profile_image.resize((round(bg_height * 0.3), round(bg_height * 0.3)))


    mask = Image.new("L", profile_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, profile_image.size[0], profile_image.size[1]), fill=255)
    profile_image.putalpha(mask)

    outline_mask = Image.new("L", profile_image.size, 0)
    draw = ImageDraw.Draw(outline_mask)
    draw.ellipse((0, 0, outline_mask.size[0], outline_mask.size[1]), fill=255)


    outline = Image.new('RGBA', outline_mask.size, (255, 255, 255, 0))
    profile_image = Image.composite(profile_image, outline, outline_mask)

    profile_position = (600, 250)

    background.paste(profile_image, profile_position, profile_image)

    draw = ImageDraw.Draw(background)

    font_size_top = int(bg_height * 0.05)
    font_top = ImageFont.truetype(font_path, font_size_top)


    draw.text((750, 650), top_text, font=font_top, fill="white", anchor="mm")

    font_size_bottom = int(bg_height * 0.05)
    font_bottom = ImageFont.truetype(font_path, font_size_bottom)


    draw.text((750, 750), bottom_text, font=font_bottom, fill="grey", anchor="mm")


    background.save(output_path, format="PNG")


#КИНТЕ ПАПКУ ASSETS В ПАПКУ СО СКРИПТОМ
#create_welcome_image("assets/black.jpg", "assets/pict.png", "Fobos зашёл на сервер!", "Участник #37", "res.png", "assets/NotoSans-Regular.ttf")
