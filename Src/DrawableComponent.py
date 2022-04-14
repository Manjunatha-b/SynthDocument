from PIL import Image, ImageDraw


class DrawableComponent():
    def __init__(self, width, height):
        self.image = Image.new('RGB', (width, height), color='white')
        self.canvas = ImageDraw.Draw(self.image)
        self.boundingBox = {}

    def getBoundingBox(self):
        return self.boundingBox

    def getImage(self):
        return self.image

    def saveImage(self, path):
        self.image.save(path)

    def __call__(self):
        return self.image, self.boundingBox
