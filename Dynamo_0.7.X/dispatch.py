#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

lst = IN[0]
pattern = IN[1]
tList, fList = [], []

for i, j in zip(lst, pattern):
	if j == 1:
		tList.append(i)
	else:
		fList.append(i)

#Assign your output to the OUT variable
OUT = tList, fList
