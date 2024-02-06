from PIL import Image, ImageDraw, ImageFont


def get_font_size_and_position(text: str, is_hindi: bool) -> tuple:
    text_length = len(text)
    if is_hindi:
        if text_length <= 20:
            return 80, (230, 110)
        elif text_length <= 25:
            return 75, (230, 115)
        elif text_length <= 30:
            return 65, (230, 125)
        elif text_length <= 35:
            return 55, (235, 135)
        else:
            return 45, (235, 140)
    else:
        if text_length <= 20:
            return 145, (220, 230)
        elif text_length <= 25:
            return 120, (215, 250)
        elif text_length <= 30:
            return 100, (210, 265)
        elif text_length <= 35:
            return 90, (210, 275)
        elif text_length <= 40:
            return 80, (205, 280)
        else:
            return 70, (200, 290)


def create_certificate(name: str, in_hindi: str, output_path: str) -> None:
    try:
        cerificate_path = "artifacts/cert_hindi.jpg" if in_hindi else "artifacts/cert_eng.jpg"
        font_path = "artifacts/font_hindi.ttf" if in_hindi else "artifacts/font_english.ttf"

        img = Image.open(cerificate_path)

        draw = ImageDraw.Draw(img)

        # text properties
        size, position = get_font_size_and_position(name, in_hindi)
        font = ImageFont.truetype(font_path, size)
        color = (0, 0, 0)

        draw.text(position, name, fill=color, font=font)

        img.save(output_path)
    except Exception as e:
        raise e
