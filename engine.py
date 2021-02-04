import qrcode 


from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

import pandas as pd

from functools import reduce


def get_default_config():
    qr_size = 40, 40
    text_size = 300, 8
    bg_size = 100, 100
    qr_pos = 30, 20
    text_pos = 0, 60
    kwargs = dict(
                       qr_size=qr_size, 
                       text_size=text_size, 
                       bg_size=bg_size, 
                       qr_pos=qr_pos, 
                       text_pos=text_pos
    )
    return kwargs

def combine_QRs(QRs):
    imgs = [i.copy() for i in QRs]
    return reduce(lambda x,y: get_concat_v(x,y), imgs)

def create_QR(mytext, kwargs=None):
    img = make_label(mytext, **kwargs)
    return img

def create_many_qr_codes(texts, kwargs=None):
    if kwargs is None:
        kwargs = get_default_config()
    qrs = []
    for text in texts:
        qr = create_QR(text, kwargs)
        qrs.append(qr)
    qr_long = combine_QRs(qrs)
    return qr_long

def get_concat_v(im1, im2):
  # https://note.nkmk.me/en/python-pillow-concat-images/
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def make_qr(mytext, w,h):
    qr = qrcode.make(mytext)
    qr = qr.resize((w,h))
    return qr

def make_text(mytext, w, h, text_color=(0,0,0)):
    font = ImageFont.truetype('arial.ttf', size=h)
    textpad = Image.new("RGB", (w, h), color=(255,255,255))
    draw = ImageDraw.Draw(textpad)
    w_text, h_text = draw.textsize(mytext)

    pos = (10,0)
    draw.text(pos, 
              mytext,
              fill=text_color, 
              font=font, 
              align = 'center',
    #           anchor = "center"
             )
    return textpad

def make_bg(w, h, bg_color=(255,255,255)):
    bg = Image.new("RGB", (w,h), color=bg_color)
    return bg

def make_label(mytext = "13l1j5n314u", qr_size=(50,50), text_size=(200,12), bg_size=(150,120), qr_pos=(50,0), text_pos=(0,60)):
    
    qr = make_qr(mytext, *qr_size)
    text = make_text(mytext, *text_size)
    bg = make_bg(*bg_size)
    bg.paste(qr, qr_pos)
    bg.paste(text, text_pos)
    return bg


# In[87]:
def main():

    qr_size = 50, 50
    text_size = 200, 12
    bg_size = 150, 80
    qr_pos = 50, 0
    text_pos = 0, 60
    kwargs = dict(
                       qr_size=qr_size, 
                       text_size=text_size, 
                       bg_size=bg_size, 
                       qr_pos=qr_pos, 
                       text_pos=text_pos
    )
    final = make_label(mytext = "12312i3m123", 
                       qr_size=qr_size, 
                       text_size=text_size, 
                       bg_size=bg_size, 
                       qr_pos=qr_pos, 
                       text_pos=text_pos)

def main2():

    qr_size = 40, 40
    text_size = 300, 8
    bg_size = 100, 100
    qr_pos = 30, 20
    text_pos = 0, 60
    kwargs = dict(
                       qr_size=qr_size, 
                       text_size=text_size, 
                       bg_size=bg_size, 
                       qr_pos=qr_pos, 
                       text_pos=text_pos
    )

    inputs = """
    qweqwoeuqwe
    qwleun12213
    qdquwne1231
    qekj12e123"""

    inputs = inputs.split("\n")
    out = create_many_qr_codes(inputs, kwargs)
    out.save("qr_code.png")

