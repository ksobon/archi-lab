import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
doc = DocumentManager.Instance.CurrentDBDocument

#Assign your output to the OUT variable
OUT = doc
