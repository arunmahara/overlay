from PIL import Image, ImageDraw, ImageFont


def get_font_size_and_position(text: str, is_hindi: bool) -> tuple:
    text_length = len(text)
    if is_hindi:
        if text_length <= 20:
            return 85, (230, 170)
        elif text_length <= 25:
            return 75, (230, 175)
        elif text_length <= 30:
            return 65, (230, 185)
        elif text_length <= 35:
            return 55, (235, 200)
        else:
            return 45, (235, 210)
    else:
        if text_length <= 20:
            return 145, (220, 220)
        elif text_length <= 25:
            return 120, (215, 240)
        elif text_length <= 30:
            return 100, (210, 260)
        elif text_length <= 35:
            return 90, (210, 270)
        elif text_length <= 40:
            return 80, (205, 275)
        else:
            return 70, (200, 280)


def create_certificate(name: str, in_hindi: str, output_path: str) -> None:
    try:
        print(f"Creating certificate for {name} and saving to {output_path}")

        cerificate_path = "artifacts/certificate_hindi.jpg" if in_hindi else "artifacts/certificate_english.jpg"
        font_path = "artifacts/font_hindi.ttf" if in_hindi else "artifacts/font_english.ttf"

        img = Image.open(cerificate_path)

        draw = ImageDraw.Draw(img)

        # text properties
        size, position = get_font_size_and_position(name, in_hindi)
        print(f"Font size: {size}, position: {position}")
        font = ImageFont.truetype(font_path, size)
        color = (0, 0, 0)

        draw.text(position, name, fill=color, font=font)

        img.save(output_path)
        print(f"Certificate created successfully to {output_path}")
    except Exception as e:
        raise e
