from PIL import Image, ImageDraw, ImageFont

def create_welcome_image(background_path, profile_image_path, top_text, bottom_text, output_path):
    # Load the background image
    background = Image.open(background_path).convert("RGBA")
    bg_width, bg_height = background.size
    background = background.resize((round(bg_width * 0.8), round(bg_height * 0.8)))

    # Load the profile image
    profile_image = Image.open(profile_image_path).convert("RGBA")
    profile_image = profile_image.resize((round(bg_height * 0.3), round(bg_height * 0.3)))  # Resize profile image

    # Make profile image circular with a white outline
    mask = Image.new("L", profile_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, profile_image.size[0], profile_image.size[1]), fill=255)
    profile_image.putalpha(mask)

    # Create a larger mask for the white outline
    outline_mask = Image.new("L", profile_image.size, 0)
    draw = ImageDraw.Draw(outline_mask)
    draw.ellipse((0, 0, outline_mask.size[0], outline_mask.size[1]), fill=255)

    # Apply the white outline
    outline = Image.new('RGBA', outline_mask.size, (255, 255, 255, 0))
    profile_image = Image.composite(profile_image, outline, outline_mask)

    profile_position = (600, 250)

    # Paste the profile image onto the background
    background.paste(profile_image, profile_position, profile_image)

    draw = ImageDraw.Draw(background)
    # Choose a font and size for the top text
    font_size_top = int(bg_height * 0.05)
    font_path_top = "assets/NotoSans-Regular.ttf" # Specify the path to your font file
    font_top = ImageFont.truetype(font_path_top, font_size_top)

    # Draw the top text
    draw.text((750, 650), top_text, font=font_top, fill="white", anchor="mm")

    # Choose a font and size for the bottom text
    font_size_bottom = int(bg_height * 0.05)
    font_path_bottom = "assets/NotoSans-Regular.ttf" # Specify the path to your font file
    font_bottom = ImageFont.truetype(font_path_bottom, font_size_bottom)

    # Draw the bottom text
    draw.text((750, 750), bottom_text, font=font_bottom, fill="grey", anchor="mm")

    # Save the result
    background.save(output_path, format="PNG")


# Create the example welcome image
create_welcome_image("assets/black.jpg", "assets/pict.png", "Fobos зашёл на сервер!", "Участник #37", "res.png")