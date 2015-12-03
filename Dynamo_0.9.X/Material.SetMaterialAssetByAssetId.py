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
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

dsCorePath = r'C:\Program Files\Dynamo 0.9\DSCoreNodes.dll'
clr.AddReferenceToFileAndPath(dsCorePath)

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

import DSCore as ds

#The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

def ProcessList(_func, _list):
	return map(lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list)

def ProcessParallelLists(_func, *lists):
	return map( lambda *xs: ProcessParallelLists(_func, *xs) if all(type(x) is list for x in xs) else _func(*xs), *lists )

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

def SetMaterialAsset(mat, assetId):
	doc = DocumentManager.Instance.CurrentDBDocument
	try:
		assetElem = doc.GetElement(assetId)
		id = assetElem.Id
		mat.AppearanceAssetId = id
		return mat
	except:
		return None
		pass

def Unwrap(item):
	return UnwrapElement(item)

if isinstance(IN[0], list):
	elements = ProcessList(Unwrap, IN[0])
else:
	elements = [Unwrap(IN[0])]

if isinstance(IN[1], list):
	assetIds = ProcessList(toRvtId, IN[1])
else:
	assetIds = [toRvtId(IN[1])]

output = []
try:
	errorReport = None
	TransactionManager.Instance.EnsureInTransaction(doc)
	output = ProcessParallelLists(SetMaterialAsset, elements, assetIds)
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
