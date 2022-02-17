import PIL.ImageDraw
import PIL.ImageFont
import os
from io import BytesIO

font = PIL.ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), "files/font.ttf"), 60
)
bg = (244, 245, 247)
fg = (30, 30, 30)


def genimg(obj):
    img = PIL.Image.new("RGB", (1200, 675), bg)
    draw = PIL.ImageDraw.Draw(img)
    draw.text((100, 80), "NEG (ネガティブ)  = {}%".format(
        obj["neg"] * 100), fill=fg, font=font)
    draw.text((100, 160), "NEU   (中立的)    = {}%".format(
        obj["neu"] * 100), fill=fg, font=font)
    draw.text((100, 240), "POS (ポジティブ)  = {}%".format(
        obj["pos"] * 100), fill=fg, font=font)
    if obj["compound"] > 0:
        gr_color = (255, 86, 86)
    elif obj["compound"] < 0:
        gr_color = (86, 86, 255)
    draw.rectangle((600, 380, 600 + int(500 * obj["compound"]), 540), fill=gr_color)
    draw.line((600, 340, 600, 580), fill=fg, width=8)
    draw.text((600, 600), ("+" if obj["compound"] > 0 else "") +
              str(obj["compound"]), fill=fg, font=font, anchor="ma")
    buff = BytesIO()
    img.save(buff, "png")
    return buff.getvalue()
