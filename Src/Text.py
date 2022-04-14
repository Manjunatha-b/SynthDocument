from string import ascii_letters
import os
import random
import textwrap
from Src.DrawableComponent import DrawableComponent
from PIL import ImageFont


class Text(DrawableComponent):
    typographySizes = {
        "header": [
            (90, 120),
            (70, 90),
            (55, 70),
        ],
        "body": [
            (16, 20),
            (14, 16),
        ]
    }

    def __init__(self,  region, typography, multiLine=True):
        super().__init__(region)
        self.typography = typography
        self.multiLine = multiLine
        self.font = self.getFont()
        self.text = "Huge text to see if it overflows into the next line properly for the multiline case and truncates for the single line case"
        self.avg_char_width = sum(self.font.getsize(
            char)[0] for char in ascii_letters) / len(ascii_letters)
        self.avg_char_height = sum(self.font.getsize(
            char)[1] for char in ascii_letters)/len(ascii_letters)

        if(self.avg_char_height > self.height):
            return

        if(self.multiLine):
            self.writeTextBox()
        else:
            self.writeTextLine()

    def getFont(self):
        fontPaths = self.getFontPathList()
        fontPath = fontPaths[random.randint(0, len(fontPaths)-1)]
        typographyBodySizeRange = self.typographySizes[self.typography][random.randint(
            0, len(self.typographySizes[self.typography])-1)]
        typographyBodySize = random.randint(
            typographyBodySizeRange[0], typographyBodySizeRange[1])
        font = ImageFont.truetype(fontPath, size=typographyBodySize)
        return font

    def getFontPathList(self):
        fonts = []
        for item in os.listdir("Fonts"):
            if(not item.startswith(".")):
                path = "Fonts/"+item
                for fontPath in os.listdir(path):
                    if(fontPath.endswith(".otf")):
                        fonts.append(path+"/"+fontPath)
        return fonts

    def writeTextLine(self):
        max_char_count = int(self.width//self.avg_char_width)
        max_lines = 1
        self.text = textwrap.wrap(self.text, width=max_char_count, max_lines=1)
        self.text = self.text[:max_lines]
        self.text = '\n'.join(self.text)
        self.canvas.text(xy=(0, 0), text=self.text,
                         font=self.font, fill='#000000')

    def writeTextBox(self,):
        max_char_count = int(self.width // self.avg_char_width)
        max_lines = int(self.height//(self.avg_char_height*1.3))
        self.text = textwrap.wrap(
            self.text, width=max_char_count, max_lines=max_lines)
        self.text = self.text[:max_lines]
        self.text = '\n'.join(self.text)
        self.canvas.text(xy=(0, 0), text=self.text,
                         font=self.font, fill='#000000')
