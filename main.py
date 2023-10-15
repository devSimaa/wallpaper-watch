from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os
import ctypes
import json

path = Path(__file__).absolute().parent


def create_wallpaper():
    current_datetime = datetime.now()
    with open(rf"{path}\config.json", 'r') as json_file:
        config = json.load(json_file)
    
    image = Image.open(f"wallpaper\{config['photo-name']}")
    width, height = image.size
    width, height = (width / 2, height / 2)


    font = ImageFont.truetype(
        font=f"fonts\{config['font']['font']}",
        size=config['font']['size']
        )

    drawer = ImageDraw.Draw(image)
    drawer.text((width-50, height-50),
f"""
'year': {current_datetime.year}
'mounth': {current_datetime.month}
'today': {current_datetime.day}
'hour': {current_datetime.hour}:{(current_datetime.minute)}

""",
                font=font,
                fill=config['font']['color'])
    
    photo_path='wallpaper\output.png'
    image.save(photo_path)
    return photo_path


def set_wallpaper():
    full_path = os.path.join(path, create_wallpaper())
    wallpaper = bytes(full_path, 'utf-8')
    ctypes.windll.user32.SystemParametersInfoA(20, 0, wallpaper, 3) # set wallpaper 



if __name__ == "__main__":
    import schedule
    import time
    schedule.every().minutes.do(set_wallpaper)
    set_wallpaper()
    while True:
        schedule.run_pending()
        time.sleep(1)
