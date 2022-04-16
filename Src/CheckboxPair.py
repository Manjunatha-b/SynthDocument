from Src.Component import Component
from Src.Text import Text
from Src.Checkbox import Checkbox

class CheckboxPair(Component):
  def __init__(self,region,orientation="left",randomPartition=False):
    super().__init__(region)
    self.orientation=orientation
    self.params = {
      "checkboxMinSize":100,
    }
    self.checkboxRegion,self.textBoxRegion = self.partitionIntoCols(region,self.params['checkboxMinSize'])
  
  def drawCheckbox(self):
    checkbox = Checkbox(self.checkboxRegion)
    text = Text(self.textBoxRegion,"body")
  
    
    