#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

lst_1 = IN[0]
lst_2 = IN[1]
pattern = IN[2]
result = []

for i, j, k in zip(lst_1, lst_2, pattern):
	if k == False:
		result.append(i)
	else:
		result.append(j)

#Assign your output to the OUT variable
OUT = result
