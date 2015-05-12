#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

input = IN[0]

total = 0
if any(isinstance(item, list) for item in input):
	input = [item for sublist in input for item in sublist]
for i in input:
	if i == None or i == "":
		total = total + 0
	else:
		if isinstance(i, str):
			total = total + int(i)
		else:
			total = total + i

#Assign your output to the OUT variable
OUT = total
