#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
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

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

keySchedule = UnwrapElement(IN[0])
data = IN[1]
inputParams = IN[2]

# "Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

count = []
cellParams = [[] for i in range(len(data))]
if any(isinstance(item, list) for item in data):
	# process list of lists
	for i in data:
		count.append(len(i))
	colCount = max(count)
	colAvailable = len(keySchedule.Definition.GetSchedulableFields())
	if colCount > colAvailable:
		message = "Please add/remove parameters to/from schedule so that they match longest data set."
	else:
		tableData = keySchedule.GetTableData()
		sectionData = tableData.GetSectionData(SectionType.Body)
		if sectionData.NumberOfRows - 2 <= len(data):
			# schedule by default will have 2 rows (A, B, C and Header Names)
			rowsToAdd = (len(data) - sectionData.NumberOfRows) + 2
			for i in range(0, rowsToAdd, 1):
				sectionData.InsertRow(0)
		else:
			# schedule when updating might already have too many rows 
			rowsToDelete = sectionData.NumberOfRows - 2 - len(data)
			for i in reversed(range(sectionData.NumberOfRows - rowsToDelete, sectionData.NumberOfRows, 1)):
				sectionData.RemoveRow(i)

# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

#Assign your output to the OUT variable
OUT = keySchedule
