#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

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
from Autodesk.Revit import *
import System

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

import os
filePath = IN[0]
identifiers = IN[1]
newNames = IN[2]
RunIt = IN[3]

files = os.listdir(filePath)

if RunIt:
	message = "Success"
	for file in files:
		currentFileName = filePath + "\\" + file
		
		for i, j in zip(identifiers, newNames):
			newFileName = filePath + "\\" + j
	
			if i in file and currentFileName != newFileName:
				try:
					os.rename(currentFileName, newFileName)
				except:
					message = "Your intended file name is not a compatible file name. Make sure that you are not strings like..."
					pass
else:
	message = "Please set RunIt to True."

#docName = uiapp.ActiveUIDocument.Document.Title
#Assign your output to the OUT variable
OUT = message
