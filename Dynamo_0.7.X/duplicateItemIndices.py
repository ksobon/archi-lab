#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

mylist = IN[0]

a, seen, result, unique = mylist, set(), [], []
for idx, item in enumerate(a):
    if item not in seen:
    	seen.add(item)
    	unique.append(idx)        
    	# First time seeing the element
    else:
    	result.append(idx)
    	# Already seen, add the index to the result

#Assign your output to the OUT variable
OUT = unique, result
