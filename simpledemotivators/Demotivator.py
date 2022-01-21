from PIL import Image, ImageDraw, ImageFont, ImageOps
import os


class Demotivator:
    def __init__(self, top_text='', bottom_text=''):
        self._top_text = top_text
        self._bottom_text = bottom_text

    def create(self, file: str) -> bool:

        font_name = (os.path.join(os.getcwd(), 'ICAD', 'simpledemotivators', 'times.ttf'))
        top_size = 80
        bottom_size = 60
        font_color = 'white'
        fill_color = 'black'

        img = Image.new('RGB', (1280, 1024), color=fill_color)
        img_border = Image.new('RGB', (1060, 720), color='#000000')
        border = ImageOps.expand(img_border, border=2, fill='#ffffff')
        user_img = Image.open(file).convert("RGBA").resize((1050, 710))
        (width, height) = user_img.size
        img.paste(border, (111, 96))
        img.paste(user_img, (118, 103))
        drawer = ImageDraw.Draw(img)

        font_1 = ImageFont.truetype(font=font_name, size=top_size, encoding='UTF-8')
        text_width = font_1.getsize(self._top_text)[0]

        while text_width >= (width + 250) - 20:
            font_1 = ImageFont.truetype(font=font_name, size=top_size, encoding='UTF-8')
            text_width = font_1.getsize(self._top_text)[0]
            top_size -= 1

        font_2 = ImageFont.truetype(font=font_name, size=bottom_size, encoding='UTF-8')
        text_width = font_2.getsize(self._bottom_text)[0]

        while text_width >= (width + 250) - 20:
            font_2 = ImageFont.truetype(font=font_name, size=bottom_size, encoding='UTF-8')
            text_width = font_2.getsize(self._bottom_text)[0]
            bottom_size -= 1

        size_1 = drawer.textsize(self._top_text, font=font_1)
        size_2 = drawer.textsize(self._bottom_text, font=font_2)

        drawer.text(((1280 - size_1[0]) / 2, 840), self._top_text, fill=font_color, font=font_1)
        drawer.text(((1280 - size_2[0]) / 2, 930), self._bottom_text, fill=font_color, font=font_2)

        img.save("output.png")
        return True
