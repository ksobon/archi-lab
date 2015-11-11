# Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

# This node was an update to Wall.Boundaries node
# that can be found in Clockwork package. Thanks
# to Andreas Dieckmann for making the original one.

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

def Unwrap(item):
	return UnwrapElement(item)

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def GetRoomBoundary(doc, item, options):
	eList = []
	cList = []
	try:
		for i in item.GetBoundarySegments(options):
			for j in i:
				eList.append(doc.GetElement(j.ElementId))
				cList.append(j.Curve.ToProtoType())
	except:
		calculator = SpatialElementGeometryCalculator(doc)
		try:
			results = calculator.CalculateSpatialElementGeometry(item)
			for face in results.GetGeometry().Faces:
				for bface in results.GetBoundaryFaceInfo(face):
					eList.append(doc.GetElement(bface.SpatialBoundaryElement.HostElementId))
		except:
			pass
	return [eList, cList]

if isinstance(IN[0], list):
	items = ProcessList(Unwrap, IN[0])
else:
	items = [Unwrap(IN[0])]

options = SpatialElementBoundaryOptions()

boundloc = AreaVolumeSettings.GetAreaVolumeSettings(doc).GetSpatialElementBoundaryLocation(SpatialElementType.Room)
options.SpatialElementBoundaryLocation = boundloc

elementList = []
curveList = []

try:
	errorReport = None
	if isinstance(items, list):
		for item in items:
			elementList.append(GetRoomBoundary(doc, item, options)[0])
			curveList.append(GetRoomBoundary(doc, item, options)[1])
	else:
		elementList = GetRoomBoundary(doc, items, options)[0]
		curveList = GetRoomBoundary(doc, items, options)[1]
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = [elementList, curveList]
else:
	OUT = errorReport
