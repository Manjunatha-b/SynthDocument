import io
import cv2
import math
import cairo
import random
import numpy as np
from PIL import Image
from imgaug import augmenters as iaa
from DrawableComponent import DrawableComponent
from imgaug.augmentables.polys import Polygon, PolygonsOnImage
# from Src.DrawableComponent import DrawableComponent


class Checkbox(DrawableComponent):
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

    def generateBox(self):
        width = 575 + random.randint(-100, 100)
        height = 575+random.randint(-100, 100)
        x, y = (700-width)//2, (700-height)//2
        r = random.randint(0, 50) if(random.random() > 0.5) else 0
        surface = cairo.SVGSurface(
            None, 700, 700)
        context = cairo.Context(surface)
        lineWidth = random.randint(5, 50) if(
            random.random() > 0.5) else random.randint(5, 10)
        context.set_line_width(lineWidth)
        context.set_source_rgb(0, 0, 0)

        context.arc(x+r, y+r, r, math.pi, 3*math.pi/2)
        context.arc(x+width-r, y+r, r, 3*math.pi/2, 0)
        context.arc(x+width-r, y+height-r, r, 0, math.pi/2)
        context.arc(x+r, y+height-r, r, math.pi/2, math.pi)
        context.close_path()
        context.stroke()
        f = io.BytesIO()
        surface.write_to_png(f)
        f.seek(0)
        self.boxImage = np.asarray(bytearray(f.read()), dtype=np.uint8)
        self.boxImage = cv2.imdecode(self.boxImage, cv2.IMREAD_UNCHANGED)[:,:,3]
        boundingPoly = PolygonsOnImage([Polygon([
            (x,y),
            (x+width,y),
            (x+width,y+height),
            (x,y+height)
        ])],self.boxImage.shape)
        self.boxImage,boundingPolyAug= self.boxAug(image=self.boxImage,polygons = boundingPoly)
        self.boxImage = cv2.cvtColor(self.boxImage,cv2.COLOR_GRAY2RGB)
        print(self.boxImage.shape)
        self.boxImage = boundingPolyAug.draw_on_image(self.boxImage)
        cv2.imwrite('bruh.png',self.boxImage)
        
        
    def generateTick(self):
        surface = cairo.SVGSurface(None, 700, 700)
        cr = cairo.Context(surface)
        lineWidth = random.randint(10, 150)
        cr.set_line_width(lineWidth)
        cr.set_source_rgb(0, 0, 0)

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

        f = io.BytesIO()
        surface.write_to_png(f)
        f.seek(0)
        self.tickImage= np.asarray(bytearray(f.read()), dtype=np.uint8)
        self.tickImage = cv2.imdecode(self.tickImage, cv2.IMREAD_UNCHANGED)[:,:,3]

    def combine(self):
        self.tickImage = self.tickAug(images=[self.tickImage])[0]
        self.boxImage = cv2.addWeighted(self.boxImage, 1, self.tickImage, 1, 0.0)
        
        

if __name__ == "__main__":
    Checkbox([(0, 0), (100, 100)])
