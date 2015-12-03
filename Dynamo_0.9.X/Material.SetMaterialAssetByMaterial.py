# Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

# Import Element wrapper extension methods
import clr
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

def ProcessList(_func, _list):
	return map(lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list)

def ProcessListArg(_func, _list, _arg):
    return map( lambda x: ProcessListArg(_func, x, _arg) if type(x)==list else _func(x, _arg), _list )

def SetMaterialAsset(mat, assetId):
	mat.AppearanceAssetId = assetId
	return mat
		
def TryGetAsset(mat):
	doc = DocumentManager.Instance.CurrentDBDocument
	appearanceId = mat.AppearanceAssetId
	if appearanceId != ElementId.InvalidElementId:
		return appearanceId
	else:
		return None

def Unwrap(item):
	return UnwrapElement(item)

if isinstance(IN[0], list):
	elements = ProcessList(Unwrap, IN[0])
else:
	elements = [Unwrap(IN[0])]

try:
	errorReport = None
	sourceMat = UnwrapElement(IN[1])
	asset = TryGetAsset(sourceMat)
	
	TransactionManager.Instance.EnsureInTransaction(doc)
	output = ProcessListArg(SetMaterialAsset, elements, asset)
	TransactionManager.Instance.TransactionTaskDone()
	
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = output
else:
	OUT = errorReport
