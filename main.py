import pyMeow as pm
import random
import time
from PIL import Image, ImageDraw, ImageFont
import hashlib
import os

class WaifuOverlay:
    def __init__(self):
        self.main_path = "S:/AI/OverlayWife" # (It was gonna use ai, but fuck that)
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
            "singing.png", "what.png", "writing_down.png", "Uhh.png",
            "Unsure.png", "Suspicious.png", "Frozen_in_ice.png", "Eating_popcorn.png",
            "Megaphone.png", "No.png", "Sleeping.png"
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
            ["I'm feeling alarmed!", "Whoa, what's happening?!", "Alert mode activated!"],                          # alarmed.png
            ["Just chilling out...", "So relaxed...", "Taking it easy."],                                           # chilling1.png
            ["So relaxed...", "Feeling calm and peaceful.", "At ease with everything."],                            # chilling2.png
            ["Still chilling...", "Hanging loose.", "Nothing to worry about."],                                     # chilling3.png
            ["A bit confused here.", "Wait, what just happened?", "Trying to figure this out."],                    # confused.png
            ["Mmm, eating time!", "Snack attack incoming!", "Deliciousness overload!"],                             # eating.png
            ["Feeling happy and jumpy!", "Can’t stop smiling!", "Energy’s through the roof!"],                      # happy_jump.png
            ["Sending kisses your way.", "Blowing you some love!", "Catch these kisses!"],                          # kisses.png
            ["You are loved.", "Remember, you matter.", "You’re appreciated."],                                     # loved.png
            ["That’s nice!", "Sounds great!", "Love to hear that!"],                                                # nice.png
            ["Please be kind.", "Kindness goes a long way.", "Spread some love today."],                            # please.png
            ["Reading a good book.", "Getting lost in a story.", "Books are magic!"],                               # reading_book.png
            ["Singing my heart out.", "Music fills my soul.", "La la la..."],                                       # singing.png
            ["What’s up?", "Hey there!", "What’s happening?"],                                                      # what.png
            ["Writing down thoughts.", "Journaling my mind.", "Putting pen to paper."],                             # writing_down.png
            ["Uhh... what just happened?", "Wait, rewind!", "Did I miss something?"],                               # Uhh.png
            ["I'm not sure about this...", "Hmm... what should I do?", "Feeling a little uncertain right now."],    # Unsure.png
            ["Hmm... I don't trust this.", "Are you sure about that?", "Something feels off..."],                   # Suspicious.png
            ["So cold... I can't move.", "Frozen solid... send help.", "Why is it always winter here?"],            # Frozen_in_ice.png
            ["Just watching it all unfold...", "This is getting interesting.", "Got my popcorn ready!"],            # Eating_popcorn.png
            ["This is important!", "Can anybody hear me?", "I'm making an announcement!"],                          # Megaphone.png
            ["No means no.", "That's a hard no.", "Not doing that."],                                               # No.png
            ["Time for a nap...", "Zzz... so cozy.", "Don’t wake me up!"],                                          # Sleeping.png
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

        texture = pm.load_texture(file_path) # Yes i know there is "load_texture_bytes" shit does not work.
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
