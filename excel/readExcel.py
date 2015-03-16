import clr
import sys
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

import System
from System import Array
from System.Collections.Generic import *

clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel

System.Threading.Thread.CurrentThread.CurrentCulture = System.Globalization.CultureInfo("en-US")
from System.Runtime.InteropServices import Marshal

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

filePath = IN[0]
runMe = IN[1]
sheetName = IN[2]
byColumn = IN[3]

if runMe:
	objExcel = Excel.ApplicationClass() 
	objExcel.Visible = False
	objExcel.DisplayAlerts = False
	objExcel.screenUpdating = False
	objExcel.Workbooks.open(str(filePath))
	
	excelWorkbook = objExcel.ActiveWorkbook
	excelSheet = objExcel.Sheets(sheetName)
	
	origin = None
	if origin == None:
		originX = excelSheet.UsedRange.Row
		originY = excelSheet.UsedRange.Column
	bound = None
	if bound == None:
		boundX = excelSheet.UsedRange.Rows(excelSheet.UsedRange.Rows.Count).Row
		boundY = excelSheet.UsedRange.Columns(excelSheet.UsedRange.Columns.Count).Column
	
	if byColumn:
		rng = excelSheet.Range[excelSheet.Cells(originX, originY), excelSheet.Cells(boundX, boundY)].Value2
		if boundY == 1:
			dataOut = [[]]
			for i in range(rng.GetLowerBound(0)-1, rng.GetUpperBound(0), 1):
					dataOut[0].append(rng[i,0])
		else:
			rng = objExcel.Transpose(rng)
			dataOut = [[] for i in range(rng.GetUpperBound(0))]
			for i in range(rng.GetLowerBound(0)-1, rng.GetUpperBound(0), 1):
				for j in range(rng.GetLowerBound(1)-1, rng.GetUpperBound(1), 1):
					dataOut[i].append(rng[i,j])
	else:
		rng = excelSheet.Range[excelSheet.Cells(originX, originY), excelSheet.Cells(boundX, boundY)].Value2
		dataOut = [[] for i in range(rng.GetUpperBound(0))]
		for i in range(rng.GetLowerBound(0)-1, rng.GetUpperBound(0), 1):
			for j in range(rng.GetLowerBound(1)-1, rng.GetUpperBound(1), 1):
				dataOut[i].append(rng[i,j])
		
	
	objExcel.ActiveWorkbook.Close(False)
	objExcel.screenUpdating = True
	Marshal.CleanupUnusedObjectsInCurrentContext()
	Marshal.ReleaseComObject(objExcel)

else:
	dataOut = "Set RunMe to True."

#Assign your output to the OUT variable
OUT = dataOut
