#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
fileExtension = IN[1]
underscore = IN[2]

newString = []
for i in IN[0]:
	newString.append(underscore.join(i) + fileExtension)
	
#Assign your output to the OUT variable
OUT = newString
