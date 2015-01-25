#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

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
from Autodesk.Revit.DB.Analysis import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

typeName = IN[0]

#get text note types
textNoteTypes = FilteredElementCollector(doc).OfClass(TextNoteType).ToElements()
bip = BuiltInParameter.ALL_MODEL_TYPE_NAME
textType = []
for i in textNoteTypes:
	if i.get_Parameter(bip).AsString() == typeName:
		textType.append(i)
	else:
		message = "Text Type with specified name \ndoes not exists. Please specify a \ndifferent name."
		
#Assign your output to the OUT variable
if len(textType) != 0:
	OUT = textType[0]
else:
	OUT = '\n'.join('{:^35}'.format(s) for s in message.split('\n'))
