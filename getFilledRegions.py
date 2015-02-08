#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Analysis import *

doc = DocumentManager.Instance.CurrentDBDocument

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

inView = FilteredElementCollector(doc, doc.ActiveView.Id).OfClass(FilledRegion)
inProject = FilteredElementCollector(doc).OfClass(FilledRegion)

#Assign your output to the OUT variable
OUT = [i.ToDSType(True) for i in inView],[j.ToDSType(True) for j in inProject]
