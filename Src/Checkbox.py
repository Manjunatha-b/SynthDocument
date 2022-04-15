import random
import math
import cairo
import io
from DrawableComponent import DrawableComponent
from PIL import Image
# from Src.DrawableComponent import DrawableComponent


class Checkbox(DrawableComponent):
    def __init__(self, region):
        super().__init__(region)
        self.isSelected = random.random() > 0.5
        self.label = {
            'Value': self.isSelected,
            'BoundingBox': [],
            'BoundingQuad': []
        }
        self.boxImage = None
        self.tickImage = None
        self.generateBox()
        if(self.isSelected):
            self.generateTick()
            self.combine()

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
        self.boxImage = Image.open(f)
        self.label['BoundingBox'] = [(x, y), (x+width, y+height)]
        self.label['BoundingQuad'] = [
            (x, y), (x+width, y), (x+width, y+height), (x, y+height)
        ]

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
        self.tickImage = Image.open(f)

    def combine(self):


if __name__ == "__main__":
    print("here")
    Checkbox([(0, 0), (1000, 1000)])
