import clr
import sys
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

#Assign your output to the OUT variable
OUT = 	["Continuous", "Dash", "DashDot", "DashDotDot", "RoundDot", "SquareDotMSO", "LongDash", "DoubleXL", "NoneXL"]
