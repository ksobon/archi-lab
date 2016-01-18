# Copyright(c) 2016, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

curve = IN[0]
type = IN[1]
view = IN[2]

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)

try:
	errorReport = None
	# get curve
	for i in curve:
		dsStartPt = i.PointAtParameter(0)
		startPt = XYZ(dsStartPt.X, dsStartPt.Y, dsStartPt.Z)
		dsEndPt = i.PointAtParameter(1)
		endPt = XYZ(dsEndPt.X, dsEndPt.Y, dsEndPt.Z)
		line = Line.CreateBound(startPt, endPt)
		# get view and symbol
		view = UnwrapElement(view)
		symbol = UnwrapElement(type)
		if symbol.Family.FamilyPlacementType == FamilyPlacementType.CurveBasedDetail:
			newFam = doc.Create.NewFamilyInstance(line, symbol, view)
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

# End Transaction
TransactionManager.Instance.TransactionTaskDone()


#Assign your output to the OUT variable
if errorReport == None:
	OUT = 0
else:
	OUT = errorReport
