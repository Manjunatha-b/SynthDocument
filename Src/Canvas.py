from PIL import Image, ImageDraw, ImageFont
from essential_generators import DocumentGenerator
from Src.Text import Text
from Src.DrawableComponent import DrawableComponent
import random
from queue import Queue


class Canvas(DrawableComponent):
    def __init__(self):
        super().__init__(1200, 1500)
        self.partitionRegions = []
        self.partitionParams = {
            "minHeight": 400,
            "minWidth": 300,
            "padRange": [10, 30],
            "divisionIterations": 4
        }
        self.partition()
        for region in self.partitionRegions:
            width = region[1][0]-region[0][0]
            height = region[1][1]-region[0][1]
            text = Text(width, height, "body", True)
            textImage, textBoundingBox = text()
            self.image.paste(textImage, region[0])

    def colorPartitions(self):
        for region in self.partitionRegions:
            color = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            self.canvas.rectangle((region[0], region[1]), fill=color)

    def padRegion(self, region):
        padRange = self.partitionParams['padRange']
        padAmount = random.randint(padRange[0], padRange[1])
        region = [(region[0][0]+padAmount, region[0][1]+padAmount),
                  (region[1][0]-padAmount, region[1][1]-padAmount)]
        return region

    def partition(self):
        bfsQueue = Queue()
        bfsQueue.put([(0, 0), (1200, 1500)])
        divisionIterations = random.randint(
            1, self.partitionParams['divisionIterations'])
        for i in range(divisionIterations):
            size = bfsQueue.qsize()
            for j in range(size):
                region = bfsQueue.get()
                if(i % 2 == 0):
                    divisionRange = [region[0][0], region[1][0]]
                    if(divisionRange[0]+self.partitionParams["minWidth"] > divisionRange[1]-self.partitionParams['minWidth']):
                        self.partitionRegions.append(self.padRegion(region))
                        continue
                    division = random.randint(
                        divisionRange[0]+self.partitionParams['minWidth'], divisionRange[1]-self.partitionParams['minWidth'])
                    bfsQueue.put([region[0], (division, region[1][1])])
                    bfsQueue.put([(division, region[0][1]), region[1]])

                else:
                    divisionRange = [region[0][1], region[1][1]]
                    if(divisionRange[0]+self.partitionParams["minHeight"] > divisionRange[1]-self.partitionParams['minHeight']):
                        self.partitionRegions.append(self.padRegion(region))
                        continue
                    division = random.randint(
                        divisionRange[0]+self.partitionParams['minHeight'], divisionRange[1]-self.partitionParams['minHeight'])
                    bfsQueue.put([region[0], (region[1][0], division)])
                    bfsQueue.put([(region[0][0], division), region[1]])

        while(not bfsQueue.empty()):
            self.partitionRegions.append(self.padRegion(bfsQueue.get()))

    def save(self, path):
        self.image.save(path, quality=100)
