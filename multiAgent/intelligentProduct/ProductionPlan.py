#from sharedInformation.PhysicalProperty import *


class ProductionPlan():
    def __init__(self):
        self.setList=[]  # initialize with empty set    
    
    def add(self, prop):
        self.setList.append(prop)
    
    def addNewSet(self, prop):
        self.setList.append(prop)
        
    def getLastSet(self):
        return self.setList[-1]
    
    def getSetList(self):
        return self.setList


#    def __str__(self) -> str:
#        output = ""
#        for s in self.set_list:
#            output += "{" + ",".join(str(prop) for prop in s) + "},"
#        return output

test=ProductionPlan()
test.add(['P11','P12'])
test.add(['P21','P22'])
print(test.getLastSet())
print(test.getSetList())



