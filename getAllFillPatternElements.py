#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr

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

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

#Assign your output to the OUT variable
OUT = FilteredElementCollector(doc).OfClass(FillPatternElement).WhereElementIsNotElementType().ToElements()
