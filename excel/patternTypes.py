import clr
import sys
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

#Assign your output to the OUT variable
OUT = 	["Solid", "75Percent", "50Percent", "25Percent", "10Percent", "Cross", "DarkDownwardDiagonal", 
		"DarkHorizontal", "DarkUpwardDiagonal", "DarkVertical", "DashedDownwardDiagonal", "DashedHorizontal", 
		"DashedUpwardDiagonal", "DashedVertical", "DiagonalBrick", "DiagonalCross", "Divot", "DottedDiamond", 
		"DottedGrid", "DownwardDiagonal", "Horizontal", "HorizontalBrick", "LargeCheckerBoard", "LargeConfetti", 
		"LargeGrid", "LightDownwardDiagonal", "LightHorizontal", "LightUpwardDiagonal", "LightVertical",
		"NarrowHorizontal", "NarrowVertical", "OutlinedDiamond", "Plaid", "Shingle", "SmallCheckerBoard", 
		"SmallConfetti", "SmallGrid", "SolidDiamond", "Sphere", "Trellis", "UpwardDiagonal", "Vertical", 
		"Wave", "Weave", "WideDownwardDiagonal", "WideUpwardDiagonal", "ZigZag"]
