class RFIDTag:
    def __init__(self, name, Type):
        self.Type = Type
        self.name = name
    
    def getID(self):
        return hash(self)
    
    def getType(self):
        return self.Type
    
    def setType(self, Type):
        self.Type = Type
    
    def __str__(self):
        return self.name + self.Type
    
    def __hash__(self):
        return hash(self.Type)
    
    def __eq__(self, other):
        if not isinstance(other, RFIDTag):
            return False
        return self.Type == other.Type
