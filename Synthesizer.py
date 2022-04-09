import os
import cairo
import math
from queue import Queue
import textwrap
from string import ascii_letters
import random
from essential_generators import DocumentGenerator
from PIL import Image,ImageDraw,ImageFont

class FontLoader():
  def __init__(self):
    self.fonts = []
    for item in os.listdir("Fonts"):
      if(not item.startswith(".")):
        path = "Fonts/"+item
        for fontPath in os.listdir(path):
          if(fontPath.endswith(".otf")):
            self.fonts.append(ImageFont.truetype(path+"/"+fontPath,size=20))

  def getFont(self):
    return self.fonts[random.randint(0,len(self.fonts)-1)]

class CheckboxGroup():
  def __init__(self,canvas,region):
    self.region = region
    self.canvas = canvas
  
  # Creating function for make roundrect shape
def roundrect(path):
  width = 575 +random.randint(-100,100)
  height = 575+random.randint(-100,100)
  x,y = (700-width)/2,(700-height)/2
  r = random.randint(0,50) if(random.random()>0.5) else 0
  with cairo.SVGSurface("temp.svg", 700, 700) as surface:
    context = cairo.Context(surface)
    lineWidth = random.randint(5,50) if(random.random()>0.5) else random.randint(5,10)
    context.set_line_width(lineWidth)
    context.set_source_rgb(0, 0, 0)

    context.arc(x+r, y+r, r,math.pi, 3*math.pi/2)
    context.arc(x+width-r, y+r, r,3*math.pi/2, 0)
    context.arc(x+width-r, y+height-r,r, 0, math.pi/2)
    context.arc(x+r, y+height-r, r,math.pi/2, math.pi)
    context.close_path()
    context.stroke()
    surface.write_to_png(path)

def correctTick(path):
  with cairo.SVGSurface("temp.svg", 700, 700) as surface:
    cr = cairo.Context(surface)
    lineWidth = random.randint(10,150)
    cr.set_line_width(lineWidth)
    cr.set_source_rgb(0, 0, 0)

    fixed = [350+random.randint(-50,50),600+random.randint(-100,0)]
    topLeft = [50+random.randint(-10,175),350+random.randint(-50,100)]
    topRight = [650+random.randint(-80,20),50+random.randint(-20,80)]
    controlLeftX = random.randint(topLeft[0],fixed[0])
    controlLeftY = random.randint(topLeft[1],fixed[1])

    controlRightX = random.randint(fixed[0],topRight[0])
    m = (topRight[1]-fixed[1])/(topRight[0]-fixed[0])
    c = fixed[1]-m*fixed[0]
    floorY = int(m*controlRightX+c)
    rightDistance = topRight[0]-fixed[0]
    rightControlDistance = controlRightX-fixed[0]
    rightControlFactor = 1-abs((rightControlDistance/rightDistance)-0.5)
    controlRightY = random.randint(topRight[1],floorY)*rightControlFactor

    if(random.random()>0.5):
      cr.set_line_join(cairo.LINE_JOIN_BEVEL)
    else:
      cr.set_line_join(cairo.LINE_JOIN_ROUND)

    if(random.random()>0.5):
      cr.set_line_cap(cairo.LINE_CAP_BUTT)
    else:
      cr.set_line_cap(cairo.LINE_CAP_ROUND)

    cr.curve_to(topLeft[0],topLeft[1],controlLeftX,controlLeftY,fixed[0],fixed[1])
    cr.curve_to(fixed[0],fixed[1],controlRightX,controlRightY,topRight[0],topRight[1])
    cr.stroke()
    
    surface.write_to_png(path)


  

    

class Canvas():
  def __init__(self):
    self.image = Image.new('RGB', (1200,1500),color='white')
    self.canvas = ImageDraw.Draw(self.image)
    self.textGenerator = DocumentGenerator()
    self.fontLoader = FontLoader()
    self.partitionRegions = []
    self.partitionParams = {
      "minHeight":400,
      "minWidth":300,
      "padRange":[10,30],
      "divisionIterations":4
    }
    self.partition()
    for region in self.partitionRegions:
      self.writeTextBox(region[0],region[1],"aasdf klasjdf ;asjdf ;askdjf ;aksjdf ;askdfj; askjdfa;skjfd a;skfj a;sdkfj a;sdkfj a;sdkfj a;sdkfj a;sdkfj a;sdkfj a;sdkfjskdlfjsldkfjlskdjfslkdjfslkdjfslkdjflskdjf slkdjflskdjf")


    

  def drawLine(self,start,end):
    print()
  
  def drawRectangle(self,start,end):
    print()
  
  def colorPartitions(self):
    for region in self.partitionRegions:
      color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
      self.canvas.rectangle((region[0],region[1]),fill=color)
      
  def padRegion(self,region):
    padRange = self.partitionParams['padRange']
    padAmount = random.randint(padRange[0],padRange[1])
    region = [(region[0][0]+padAmount,region[0][1]+padAmount),(region[1][0]-padAmount,region[1][1]-padAmount)]
    return region
  
  def partition(self):
    bfsQueue = Queue() 
    bfsQueue.put([(0,0),(1200,1500)])
    divisionIterations = random.randint(1,self.partitionParams['divisionIterations'])
    for i in range(divisionIterations):
      size = bfsQueue.qsize()
      for j in range(size):
        region = bfsQueue.get()
        if(i%2==0):
          divisionRange = [region[0][0],region[1][0]]
          if(divisionRange[0]+self.partitionParams["minWidth"]>divisionRange[1]-self.partitionParams['minWidth']):
            self.partitionRegions.append(self.padRegion(region))
            continue
          division = random.randint(divisionRange[0]+self.partitionParams['minWidth'],divisionRange[1]-self.partitionParams['minWidth'])
          bfsQueue.put([region[0],(division,region[1][1])])
          bfsQueue.put([(division,region[0][1]),region[1]])

        else:
          divisionRange = [region[0][1],region[1][1]]
          if(divisionRange[0]+self.partitionParams["minHeight"]>divisionRange[1]-self.partitionParams['minHeight']):
            self.partitionRegions.append(self.padRegion(region))
            continue
          division = random.randint(divisionRange[0]+self.partitionParams['minHeight'],divisionRange[1]-self.partitionParams['minHeight'])
          bfsQueue.put([region[0],(region[1][0],division)])
          bfsQueue.put([(region[0][0],division),region[1]])
    
    while(not bfsQueue.empty()):
      self.partitionRegions.append(self.padRegion(bfsQueue.get()))
          
  
  def writeTextBox(self,start,end,text):
    width = end[0]-start[0]
    height = end[1]-start[1]
    font = self.fontLoader.getFont()
    avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
    avg_char_height = sum(font.getsize(char)[1] for char in ascii_letters)/len(ascii_letters)
    max_char_count = int(width / avg_char_width)
    max_lines = int(height//(avg_char_height*1.3))
    text = self.textGenerator.paragraph()
    text = textwrap.wrap(text,width=max_char_count,max_lines=max_lines)
    text = text[:max_lines]
    text = '\n'.join(text)
    self.canvas.text(xy=start, text=text, font=font, fill='#000000')
  
  def save(self,path):
    self.image.save(path,quality=100)
    


class Synthesizer():
  def __init__(self):
    self.canvas = Canvas()
    
    self.canvas.save('result.png')
    



Synthesizer()