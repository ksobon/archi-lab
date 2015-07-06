#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

sheets = IN[0]
pRange = IN[1]
combined = IN[2]
printerName = IN[3]
printSetting = IN[4]
filePath = IN[5]
runIt = IN[6]

message = "Success"
if runIt:
	viewSheets = []
	for i in sheets:
		viewSheets.append(UnwrapElement(i))
	
	viewSet = ViewSet()
	if isinstance(sheets, list):
		for i in sheets:
			viewSheet = UnwrapElement(i)
			viewSet.Insert(viewSheet)
	else:
		viewSheet = UnwrapElement(sheets)
		viewSet.Insert(viewSheet)
	
	printManager = doc.PrintManager
	printManager.PrintRange = pRange
	printManager.Apply()
	viewSheetSetting = printManager.ViewSheetSetting
	viewSheetSetting.CurrentViewSheetSet.Views = viewSet
	
	printManager.SelectNewPrintDriver(printerName)
	printManager.Apply()
	if printManager.IsVirtual:
		printManager.CombinedFile = combined
		printManager.Apply()
		printManager.PrintToFile = True
		printManager.Apply()
	else:
		printManager.CombinedFile = combined
		printManager.Apply()
		printManager.PrintToFile = False
		printManager.Apply()
	
	printManager.PrintToFileName = filePath
	printManager.Apply()

	ps = FilteredElementCollector(doc).OfClass(PrintSetting)
	for i in ps:
		if i.Name == printSetting:
			newPrintSetting = i
	try:
		printSetup = printManager.PrintSetup
		printSetup.CurrentPrintSetting = newPrintSetting
		printManager.Apply()
	except:
		pass
			
	# Start Transaction
	doc = DocumentManager.Instance.CurrentDBDocument
	TransactionManager.Instance.EnsureInTransaction(doc)
	
	viewSheetSetting.SaveAs("tempSetName")
	printManager.Apply()
	printManager.SubmitPrint()
	viewSheetSetting.Delete()
	
	# End Transaction
	TransactionManager.Instance.TransactionTaskDone()
else:
	message = "Set RunIt to True"

#Assign your output to the OUT variable
OUT = message
