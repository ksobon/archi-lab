import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

def ListContains(item, filter):
	if item in filter:
		return True
	else:
		return False

def ProcessListArg(_func, _list, _arg):
	return map( lambda x: processListArg(_func, x, _arg) if type(x)==list else _func(x, _arg), _list )

#Assign your output to the OUT variable
OUT = ProcessListArg(ListContains, IN[0], IN[1])
