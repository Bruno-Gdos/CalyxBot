import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from  qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from PIL import Image, ImageDraw
import discord
import os
from io import BytesIO
import base64


CALYX_ICON_PATH = "Calyx.png"


def style_eyes(img):
    img_size = img.size[0]
    eye_size = 70 #default
    quiet_zone = 40 #default
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((40, 40, 110, 110), fill=255)
    draw.rectangle((img_size-110, 40, img_size-40, 110), fill=255)
    draw.rectangle((40, img_size-110, 110, img_size-40), fill=255)
    return mask

async def  qr_generator (content :str, timestamp, ctx):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(content)
    await ctx.send(f"{ctx.author.mention} Gerando QR Code...")

    img = qr.make_image(image_factory=StyledPilImage, embeded_image_path=CALYX_ICON_PATH, module_drawer=RoundedModuleDrawer())
    img.save("qrCode.png")


    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(content)

    qr_eyes_img = qr.make_image(image_factory=StyledPilImage,
                                color_mask=SolidFillColorMask(front_color=(231, 190, 63))
                                )
    
    qr_img = qr.make_image(image_factory=StyledPilImage,
                        module_drawer=CircleModuleDrawer(),
                        color_mask=SolidFillColorMask(front_color=(59, 89, 152)),
                        embeded_image_path=CALYX_ICON_PATH)

    mask = style_eyes(qr_img)
    final_img = Image.composite(qr_eyes_img, qr_img, mask)
    temp = BytesIO()
    final_img.save(temp, format="png")
    temp.seek(0)
    await ctx.send(file=discord.File(temp, filename='qrCode.png'))
