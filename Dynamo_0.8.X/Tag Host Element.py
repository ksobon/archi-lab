#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import Element wrapper extension methods
clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager and TransactionManager
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

# Import RevitAPI
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

if isinstance(IN[0], list):
	elem = [UnwrapElement(i) for i in IN[0]]
else:
	elem = [UnwrapElement(IN[0])]

def ProcessList(_func, _list):
    return map( lambda x:
    process_list(_func, x) if type(x)==list else _func(x), _list )

def GetHostElement(tag):
	doc = DocumentManager.Instance.CurrentDBDocument
	hostElemId = tag.TaggedLocalElementId
	hostElem = doc.GetElement(hostElemId)
	return hostElem

try:
	errorReport = None
	output = ProcessList(GetHostElement, elem)
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = output
else:
	OUT = errorReport
