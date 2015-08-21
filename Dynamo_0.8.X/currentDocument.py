# Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

# Import DocumentManager
import clr
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

try:
	errorReport = None
	doc = DocumentManager.Instance.CurrentDBDocument
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = doc
else:
	OUT = errorReport
