#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
import sys
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

from Autodesk.DesignScript.Geometry import *
import System

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
designOptionId = IN[0]
_invert = IN[1]
_category = IN[2]

# conversion from integer to ElementId
def toRvtId(_id):
	if isinstance(_id, int) or isinstance(_id, str):
		id = ElementId(int(_id))
		return id
	elif isinstance(_id, ElementId):
		return _id

optionId = toRvtId(designOptionId)

# if filter is inverted it will collect elemets not in design option
if not _invert:
	filter = ElementDesignOptionFilter(optionId, False)
else:
	filter = ElementDesignOptionFilter(optionId, True)

# retrieve elements of given category for specified design option
builtInCategory = System.Enum.ToObject(BuiltInCategory, _category.Id)
elementsDesignOption = FilteredElementCollector(doc).WherePasses(filter).OfCategory(builtInCategory).WhereElementIsNotElementType().ToElements()
	
#Assign your output to the OUT variable
OUT = elementsDesignOption
