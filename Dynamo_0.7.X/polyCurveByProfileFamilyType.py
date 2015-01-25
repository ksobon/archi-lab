#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

from System.Collections.Generic import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
#name = str(IN[0].Name)
type = UnwrapElement(IN[0].Family.Name)
name = UnwrapElement(IN[0].Name)

#select family instance by name
families = FilteredElementCollector(doc).OfClass(Family)

allTypeNames = []
for i in families:
	familyTypeSet = i.Symbols
	elemIter = familyTypeSet.ForwardIterator()
	elemIter.Reset()
	while elemIter.MoveNext():
		curElem = elemIter.Current
		if curElem.ToDSType(True).Name == name and i.Name == type:
			family = curElem.Family

#extract profile curves from family(sketch)
message = None
try:
	famDoc = doc.EditFamily(family)
	famCollector = FilteredElementCollector(famDoc)
	sketch = famCollector.OfClass(Sketch)
	#convert revit geometry to DS Geometry (lines, arc etc)
	for i in sketch:
		cArray = list(i.Profile)
	cArray[:] = [[Revit.GeometryConversion.RevitToProtoCurve.ToProtoType(y, True ) for y in x] for x in cArray]
except:
	message = "Could not obtain this family. \nPossible reasons: System Family, \nFamily does not contain sketch loops \n(simple profile family)"
	pass

#Assign your output to the OUT variable
if message == None:
	OUT = cArray
else:
	OUT = '\n'.join('{:^35}'.format(s) for s in message.split('\n'))
