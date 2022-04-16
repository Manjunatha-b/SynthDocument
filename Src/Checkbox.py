import io
import cv2
import math
import cairo
import random
import numpy as np
from math import ceil
from PIL import Image
from imgaug import augmenters as iaa
from imgaug.augmentables.polys import Polygon, PolygonsOnImage
from Src.Component import Component


class Checkbox(Component):
    def __init__(self, region):
        super().__init__(region)
        self.isSelected = random.random() > 0.5
        self.label = {
            'Value': self.isSelected,
            'BoundingPoly': [],
        }
        self.boxImage = None
        self.tickImage = None

        self.boxAug =  iaa.Affine(rotate=(-1.5, 1.5),translate_percent=(0.025,0.025), scale=(0.8,1))
        self.tickAug = iaa.Affine(rotate=(-10, 10),translate_percent=(0.05,0.05),scale=(0.7,1.1))

        self.generateBox()
        if(self.isSelected):
            self.generateTick()
            self.combine()
        
        self.boxImage = 255-self.boxImage
    
    def getImageGivenSurface(self,surface):
        f = io.BytesIO()
        surface.write_to_png(f)
        f.seek(0)
        image = np.asarray(bytearray(f.read()), dtype=np.uint8)
        image = cv2.imdecode(image,cv2.IMREAD_UNCHANGED)[:,:,3]
        return image

    def generateBox(self):
        width = 575 + random.randint(-100, 100)
        height = 575+random.randint(-100, 100)
        x, y = (700-width)//2, (700-height)//2
        r = random.randint(0, 50) if(random.random() > 0.5) else 0
        lineWidth = random.randint(5, 50) if(
            random.random() > 0.5) else random.randint(5, 10)
        halfLineWidth = ceil(lineWidth/2)
        surface = cairo.SVGSurface(None, 700, 700)
        context = cairo.Context(surface)

        def initSurface():
            context.set_line_width(lineWidth)
            context.set_source_rgb(0, 0, 0)

        def draw():
            context.arc(x+r, y+r, r, math.pi, 3*math.pi/2)
            context.arc(x+width-r, y+r, r, 3*math.pi/2, 0)
            context.arc(x+width-r, y+height-r, r, 0, math.pi/2)
            context.arc(x+r, y+height-r, r, math.pi/2, math.pi)
            context.close_path()
            context.stroke()
        
        initSurface()
        draw()
        self.boxImage = self.getImageGivenSurface(surface)
        self.poly = PolygonsOnImage([Polygon([
            (x-halfLineWidth,y-halfLineWidth),
            (x+width+halfLineWidth,y-halfLineWidth),
            (x+width+halfLineWidth,y+height+halfLineWidth),
            (x-halfLineWidth,y+height+halfLineWidth)
        ])],self.boxImage.shape)
        
        
    def generateTick(self):
        lineWidth = random.randint(10, 150)
        fixed = [350+random.randint(-50, 50),
                 600+random.randint(-100, 0)]
        topLeft = [
            50+random.randint(-10, 175), 350+random.randint(-50, 100)]
        topRight = [
            650+random.randint(-80, 20), 50+random.randint(-20, 80)]
        controlLeftX = random.randint(topLeft[0], fixed[0])
        controlLeftY = random.randint(topLeft[1], fixed[1])
        controlRightX = random.randint(fixed[0], topRight[0])
        m = (topRight[1]-fixed[1])/(topRight[0]-fixed[0])
        c = fixed[1]-m*fixed[0]
        floorY = int(m*controlRightX+c)
        rightDistance = topRight[0]-fixed[0]
        rightControlDistance = controlRightX-fixed[0]
        rightControlFactor = 1 - \
            abs((rightControlDistance/rightDistance)-0.5)
        controlRightY = random.randint(
            topRight[1], floorY)*rightControlFactor
        surface = cairo.SVGSurface(None, 700, 700)
        cr = cairo.Context(surface)
        
        def initSurface():
            cr.set_line_width(lineWidth)
            cr.set_source_rgb(0, 0, 0)
    
        def draw():
            if(random.random() > 0.5):
                cr.set_line_join(cairo.LINE_JOIN_BEVEL)
            else:
                cr.set_line_join(cairo.LINE_JOIN_ROUND)

            if(random.random() > 0.5):
                cr.set_line_cap(cairo.LINE_CAP_BUTT)
            else:
                cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.curve_to(topLeft[0], topLeft[1], controlLeftX,
                        controlLeftY, fixed[0], fixed[1])
            cr.curve_to(fixed[0], fixed[1], controlRightX,
                        controlRightY, topRight[0], topRight[1])
            cr.stroke()
        
        initSurface()
        draw()
        self.tickImage = self.getImageGivenSurface(surface)

    def combine(self):
        self.tickImage = self.tickAug(images=[self.tickImage])[0]
        self.boxImage,self.poly= self.boxAug(image=self.boxImage,polygons = self.poly)
        self.boxImage = cv2.addWeighted(self.boxImage, 1, self.tickImage, 1, 0.0)
        
        

if __name__ == "__main__":
    Checkbox([(0, 0), (100, 100)])
