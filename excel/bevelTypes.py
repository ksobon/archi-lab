import clr
import sys
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

#Assign your output to the OUT variable
OUT = 	["None", "Angle", "ArtDeco", "Circle", "Convex", "CoolSlant", "Cross", "Divot", "HardEdge", "RelaxedInset", 
		"Riblet", "Slope", "SoftRound"]
