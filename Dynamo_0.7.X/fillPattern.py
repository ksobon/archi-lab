#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

from System.Collections.Generic import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

name = str(IN[0])
drafting = IN[1]

message = None
if drafting:
	fillPatTarget = FillPatternTarget.Drafting
else:
	fillPatTarget = FillPatternTarget.Model

try:
	fillPat = FillPatternElement.GetFillPatternElementByName(doc, fillPatTarget, name)
	message = "Specified name and pattern type \n(drafting/model) do not match. \nPlease check your spelling."
except:
	message = "Specified name and pattern type (drafting/model) do not match. \nPlease check your spelling."
	pass

#Assign your output to the OUT variable
if fillPat != None:
	OUT = fillPat.ToDSType(True)
else:
	OUT = '\n'.join('{:^35}'.format(s) for s in message.split('\n'))
