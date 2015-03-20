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

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

import os.path

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

filePath = IN[0]
runMe = IN[1]
sheetName = IN[2]
byColumn = IN[3]
data = IN[4]
liveStreaming = IN[5]

def LiveStream():
	try:
		xlApp = Marshal.GetActiveObject("Excel.Application")
		xlApp.Visible = True
		xlApp.DisplayAlerts = True
		xlApp.ScreenUpdating = True
		return xlApp
	except:
		return None

def GetWorkbook(xlApp, filePath):
	if os.path.isfile(str(filePath)):
		xlApp.Workbooks.open(str(filePath))
		wb = xlApp.ActiveWorkbook
		return wb
	else:
		wb = xlApp.Workbooks.Add()
		return wb

def GetWorksheet(xlApp, filePath, sheetName):
	if os.path.isfile(str(filePath)):
		xlApp.Workbooks.open(str(filePath))
		ws = xlApp.Sheets(sheetName)
		ws.Cells.ClearContents()
		ws.Cells.Clear()
		return ws
	else:
		wb = xlApp.Workbooks.Add()
		ws = wb.Worksheets[1]
		return ws

def WriteData(ws, data, byColumn):
	originX = ws.UsedRange.Row
	originY = ws.UsedRange.Column
	boundX = len(data)
	boundY = len(data[0])
	if byColumn:
		for x in range(0, len(data), 1):
			for y in range(0, len(data[0]), 1):
				ws.Cells[y+1, x+1] = data[x][y]
	else:
		for x in range(0, len(data), 1):
			for y in range(0, len(data[0]), 1):
				ws.Cells[x+1,y+1] = data[x][y]
	return ws

if runMe:
	message = None
	if liveStreaming:
		if LiveStream() == None:
			message = "Please open an excel session for Live Stream"
		else:
			xlApp = LiveStream()
			wb = xlApp.ActiveWorkbook
			ws = xlApp.ActiveSheet
			ws.Cells.ClearContents()
			ws.Cells.Clear()
			WriteData(ws, data, byColumn)
	else:
		# check if excel is open if its open close it before doing all this
		# otherwise it will throw an error
		
		xlApp = Excel.ApplicationClass()
		xlApp.Visible = False
		xlApp.DisplayAlerts = False
		xlApp.ScreenUpdating = False
		wb = GetWorkbook(xlApp, filePath)
		ws = GetWorksheet(xlApp, filePath, sheetName)
		WriteData(ws, data, byColumn)
		wb.SaveAs(str(filePath))
		xlApp.ActiveWorkbook.Close(False)
		xlApp.screenUpdating = True
		Marshal.CleanupUnusedObjectsInCurrentContext()
		Marshal.ReleaseComObject(xlApp)

	"""
	rng = ws.Range[ws.Cells(originX, originY), ws.Cells(boundX, boundY)].Value2
	arr = Array.CreateInstance(int, boundX, boundY)
	for i in range(0, len(data),1):
		for j in range(0,len(data[0]), 1):
			arr.SetValue(data[i][j], i,j)
	rng = arr
	"""

#Assign your output to the OUT variable
if message == None:
	OUT = "Success!"
else:
	OUT = message
