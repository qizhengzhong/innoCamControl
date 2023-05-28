class Part:
    
    def __init__(self, tag):        
        self.WindingRule = 0
        self.size = 5
        self.color = 'black'
        self.shape='square'
        
        #self.shape.setWindingRule(0)
        self.tag = tag
    
    def getRFIDTag(self):
        return self.tag
    
    def setRFIDTag(self, tag):
        self.tag = tag
    
    def getShape(self):
        return self.shape
    
    def setShape(self, shape):
        self.shape = shape
    
    def changeShape(self, shape):
        self.shape.append(shape, False)
    
    def getSize(self):
        return self.size
    
    def setSize(self, newScale):
        self.size = newScale
    
    def getColor(self):
        return self.color
    
    def setColor(self, color):
        self.color = color
    
    def getWindingRule(self):
        return self.WindingRule
    
    def setWindingRule(self, windingRule):
        self.WindingRule = windingRule
    
    def __str__(self):
        return "Part" + str(self.tag)
