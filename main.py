import pyMeow as pm
import random
import time
from PIL import Image, ImageDraw, ImageFont
import hashlib
import os

class WaifuOverlay:
    def __init__(self):
        self.main_path = "S:/AI/OverlayWife"
        title = "Waifu"
        pm.overlay_init(target=title, title=title, fps=10)
        self.color = pm.get_color("white")
        self.font = self.main_path + "/fonts/YellowSun.otf"
        temp_folder = self.main_path + "/temp"
        self.text_cache = {
            filename[len("text_"):-len(".png")]: pm.load_texture(os.path.join(temp_folder, filename))
            for filename in os.listdir(temp_folder) if filename.endswith(".png")
        }

        self.choices = [
            "alarmed.png", "chilling1.png", "chilling2.png", "chilling3.png",
            "confused.png", "eating.png", "happy_jump.png", "kisses.png",
            "loved.png", "nice.png", "please.png", "reading_book.png",
            "singing.png", "what.png", "writing_down.png", "Uhh.png"
        ]
        self.textures = [pm.load_texture(self.main_path + f"/images/{choice}") for choice in self.choices]

        self.posX = 1461
        self.posY = 880
        self.rotation = 0
        self.scale = 0.3
        self.text_scale = 100

        self.current_index = 0
        self.current_index2 = 0
        self.last_switch_time = time.time()
        self.switch_interval = 7

        self.messages = [
            ["I'm feeling alarmed!", "Whoa, what's happening?!", "Alert mode activated!"],
            ["Just chilling out...", "So relaxed...", "Taking it easy."],
            ["So relaxed...", "Feeling calm and peaceful.", "At ease with everything."],
            ["Still chilling...", "Hanging loose.", "Nothing to worry about."],
            ["A bit confused here.", "Wait, what just happened?", "Trying to figure this out."],
            ["Mmm, eating time!", "Snack attack incoming!", "Deliciousness overload!"],
            ["Feeling happy and jumpy!", "Can’t stop smiling!", "Energy’s through the roof!"],
            ["Sending kisses your way.", "Blowing you some love!", "Catch these kisses!"],
            ["You are loved.", "Remember, you matter.", "You’re appreciated."],
            ["That’s nice!", "Sounds great!", "Love to hear that!"],
            ["Please be kind.", "Kindness goes a long way.", "Spread some love today."],
            ["Reading a good book.", "Getting lost in a story.", "Books are magic!"],
            ["Singing my heart out.", "Music fills my soul.", "La la la..."],
            ["What’s up?", "Hey there!", "What’s happening?"],
            ["Writing down thoughts.", "Journaling my mind.", "Putting pen to paper."],
            ["Uhh... what just happened?", "Wait, rewind!", "Did I miss something?"]
        ]

    def text_to_texture(self, text, font_path, font_size, color):
        key = f"{text}_{font_size}_{color}"
        if key in self.text_cache:
            return self.text_cache[key]

        font = ImageFont.truetype(font_path, font_size)
        dummy_img = Image.new("RGBA", (1, 1))
        draw = ImageDraw.Draw(dummy_img)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
        img = Image.new("RGBA", text_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, font=font, fill=color)

        hashed_key = hashlib.md5(key.encode()).hexdigest()
        file_path = self.main_path + f"/temp/text_{hashed_key}.png"
        img.save(file_path)

        texture = pm.load_texture(file_path)
        self.text_cache[key] = texture
        return texture

    def DrawAnimeGirl(self, texture):
        pm.draw_texture(texture, self.posX, self.posY,
                        self.color, self.rotation, self.scale)

    def Waifu(self):
        now = time.time()
        if now - self.last_switch_time > self.switch_interval:
            self.current_index = random.randint(0, len(self.textures) - 1)
            self.current_index2 = random.randint(0, len(self.messages[self.current_index]) - 1)
            self.last_switch_time = now

        texture = self.textures[self.current_index]
        self.DrawAnimeGirl(texture)

        text = self.messages[self.current_index][self.current_index2]
        text_texture = self.text_to_texture(text, self.font, self.text_scale, (255, 182, 193))
        pm.draw_texture(text_texture, self.posX - 20, self.posY - 35, self.color, self.rotation, 0.3)

    def main(self):
        while pm.overlay_loop():
            pm.begin_drawing()
            self.Waifu()
            pm.end_drawing()

if __name__ == "__main__":
    waifu = WaifuOverlay()
    waifu.main()
