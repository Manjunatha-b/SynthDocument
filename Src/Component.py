import random
from PIL import Image, ImageDraw
from imgaug.augmentables import Polygon
from numpy import partition

TYPES = [
    "bundler",
    "checkbox",
    "checkboxPair",
    "key",
    "value",
    "keyValuePair",
    "text"
]

class Component():
    def __init__(self, region):
        self.width = region[1][0]-region[0][0]
        self.height = region[1][1]-region[0][1]
        self.image = Image.new('RGB', (self.width, self.height), color='white')
        self.canvas = ImageDraw.Draw(self.image)
        self.poly = None
        self.children = []

    def getLabel(self):
        return self.label

    def getImage(self):
        return self.image
    
    def partitionIntoRows(self,region,minHeight,maxHeight):
        regions = []
        height = region[1][1]-region[0][1]
        start = region[1]
        while(start[1]<height):
            partitionHeight = random.randint(minHeight,maxHeight)
            partitionRegion = [(region[0][0],start),(region[1][0],start+partitionHeight)]
            start+=partitionHeight
            regions.append(partitionRegion)
        print(regions)
    
    def biPartitionCol(self,region,partitionWidth):
        regionOne = [
            region[0],
            (region[0][0]+partitionWidth,region[1][1])
        ]    
        regionTwo = [
            (region[0][0]+partitionWidth,region[0][1]),
            region[1]
        ]
        return regionOne,regionTwo

    def partitionIntoCols(self,region,minWidth):
        regions = []



    def saveImage(self, path):
        self.image.save(path)

    def __call__(self):
        return self.image, self.poly

