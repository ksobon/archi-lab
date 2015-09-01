# Copyright(c) 2015, Konrad Sobon
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

from System.Collections.Generic import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
doc = IN[1]

def toRvtId(_id):
	if isinstance(_id, int):
		id = ElementId(int(_id))
		return id
	elif isinstance(_id, str) and len(_id) > 7:
		return _id
	elif isinstance(_id, str) and len(_id) < 7:
		id = ElementId(int(_id))
		return id
	elif isinstance(_id, Autodesk.Revit.DB.ElementId):
		return _id

#unwrap incoming information for use with API
ids = []
for i in IN[0]:
    ids.append(UnwrapElement(i))

try:
	errorReport = None
	elements = []
	for i in ids:
		elements.append(doc.GetElement(toRvtId(i)).ToDSType(True))
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = elements
else:
	OUT = errorReport
