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
_tcs = IN[1]

#"Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

if _tcs != None:
	tableData = keySchedule.GetTableData()
	hsd = tableData.GetSectionData(SectionType.Header)
	hsd.SetCellText(hsd.FirstRowNumber, hsd.FirstColumnNumber, _tcs[1])
	if _tcs[0] != None:
		if hsd.AllowOverrideCellStyle(hsd.FirstRowNumber, hsd.FirstColumnNumber):
			hsd.SetCellStyle(hsd.FirstRowNumber, hsd.FirstColumnNumber, _tcs[0])

# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

#Assign your output to the OUT variable
OUT = 0
