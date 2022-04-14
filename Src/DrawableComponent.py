from PIL import Image, ImageDraw


class DrawableComponent():
    def __init__(self, region):
        self.width = region[1][0]-region[0][0]
        self.height = region[1][1]-region[0][1]
        self.image = Image.new('RGB', (self.width, self.height), color='white')
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
