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
from RevitServices.Transactions import TransactionManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

from System.Collections.Generic import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import re

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

keySchedule = UnwrapElement(IN[0])
data = IN[1]
inputParams = IN[2]
upper = IN[3]

# "Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

tableData = keySchedule.GetTableData()
sectionData = tableData.GetSectionData(SectionType.Body)

keyNames = []
for i in range(1,sectionData.NumberOfRows - 1,1):
	keyNames.append(str(int(i)))

allKeys = FilteredElementCollector(doc).WhereElementIsNotElementType()
params = [[] for i in range(len(keyNames))]

for key in allKeys:
	try:
		if key.get_Parameter(BuiltInParameter.REF_TABLE_ELEM_NAME).AsString() in keyNames and key.OwnerViewId == keySchedule.Id:
			indexValue = keyNames.index(key.get_Parameter(BuiltInParameter.REF_TABLE_ELEM_NAME).AsString())
			for i in range(0, len(inputParams),1):
						params[indexValue].append(key.get_Parameter(str(inputParams[i])))
	except:
		pass

for i, j in zip(params, data):
	for param, value in zip(i,j):
		if isinstance(value, str):
			valueDecoded = value.decode('string_escape')
		else:
			if value == None:
				valueDecoded = " "
			else:
				valueDecoded = str(value).decode('string_escape')
		if upper:
			valueDecoded = valueDecoded.upper()
			param.Set(valueDecoded)
		else:
			param.Set(valueDecoded)


# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

#Assign your output to the OUT variable
OUT = 0
