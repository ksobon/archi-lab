#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

input = IN[0]

def ProcessList(_func, _list):
	return map(lambda x: ProcessList(_func, x) if type(x) == list else _func(x), _list)

def ConvertToInteger(item):
	if item == None:
		return 0
	elif type(item) == str:
		if item == "":
			return 0
		else:
			return int(item)
	else:
		return item

input = ProcessList(ConvertToInteger, input)
if any(isinstance(item,list) for item in input):
	output = map(sum,input)
else:
	output = sum(input)

#Assign your output to the OUT variable
OUT = output
