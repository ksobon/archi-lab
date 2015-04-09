import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

def UpperCase(string):
	return string.upper()
def process_list(_func, _list):
    return map( lambda x: process_list(_func, x) if type(x)==list else _func(x), _list )

#Assign your output to the OUT variable
OUT = process_list(UpperCase, IN[0])
