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

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

sheets = IN[0]
pRange = IN[1]
combined = IN[2]
printerName = IN[3]
printSetting = IN[4]
filePath = IN[5]
runIt = IN[6]

if isinstance(sheets, list):
	viewSheets = []
	for i in sheets:
		viewSheets.append(UnwrapElement(i))
else:
	viewSheets = UnwrapElement(sheets)

def PrintView(doc, sheet, pRange, printerName, combined, filePath, printSetting):
	# create view set 
	viewSet = ViewSet()
	viewSet.Insert(sheet)
	# determine print range
	printManager = doc.PrintManager
	printManager.PrintRange = pRange
	printManager.Apply()
	# make new view set current
	viewSheetSetting = printManager.ViewSheetSetting
	viewSheetSetting.CurrentViewSheetSet.Views = viewSet
	# set printer
	printManager.SelectNewPrintDriver(printerName)
	printManager.Apply()
	# set combined and print to file
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
	# set file path
	printManager.PrintToFileName = filePath
	printManager.Apply()
	# apply print setting
	try:
		printSetup = printManager.PrintSetup
		printSetup.CurrentPrintSetting = printSetting
		printManager.Apply()
	except:
		pass
	# save settings and submit print
	TransactionManager.Instance.EnsureInTransaction(doc)
	viewSheetSetting.SaveAs("tempSetName")
	printManager.Apply()
	printManager.SubmitPrint()
	viewSheetSetting.Delete()
	TransactionManager.Instance.TransactionTaskDone()
	
	return True

try:
	errorReport = None
	message = "Success"
	if runIt:
		if isinstance(viewSheets, list) and isinstance(printSetting, list):
			for i, j in zip(viewSheets, printSetting):
				PrintView(doc, i, pRange, printerName, combined, filePath, j)
		elif isinstance(viewSheets, list) and not isinstance(printSetting, list):
			for i in viewSheets:
				PrintView(doc, i, pRange, printerName, combined, filePath, printSetting)
		elif not isinstance(viewSheets, list) and not isinstance(printSetting, list):
			PrintView(doc, viewSheets, pRange, printerName, combined, filePath, printSetting)
	else:
		message = "Set RunIt to True"
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()
	
#Assign your output to the OUT variable
if errorReport == None:
	OUT = message
else:
	OUT = errorReport
