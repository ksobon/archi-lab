# Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

# Import DocumentManager
import clr
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

#Assign your output to the OUT variable
OUT = doc
