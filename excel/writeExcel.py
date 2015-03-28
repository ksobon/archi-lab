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
cellFill = IN[6]
borderStyle = IN[7]

# Fill Settings definitions
def GetLineStyle(key):
	keys = ["Continuous", "Dash", "DashDot", "DashDotDot", "RoundDot", "SquareDotMSO", "LongDash", 
			"DoubleXL", "NoneXL"]
	values = [1, -4115, 4, 5, -4118, -4118, -4115, -4119, -4142]
	d = dict()
	for i in range(len(keys)):
		d[keys[i]] = values[i]
	if key in d:
		return d[key]
	else:
		return None

def GetPatternType(key):
	keys = ["Solid", "75Percent", "50Percent", "25Percent", "10Percent", "Cross", "DarkDownwardDiagonal", 
		"DarkHorizontal", "DarkUpwardDiagonal", "DarkVertical", "DashedDownwardDiagonal", "DashedHorizontal", 
		"DashedUpwardDiagonal", "DashedVertical", "DiagonalBrick", "DiagonalCross", "Divot", "DottedDiamond", 
		"DottedGrid", "DownwardDiagonal", "Horizontal", "HorizontalBrick", "LargeCheckerBoard", "LargeConfetti", 
		"LargeGrid", "LightDownwardDiagonal", "LightHorizontal", "LightUpwardDiagonal", "LightVertical",
		"NarrowHorizontal", "NarrowVertical", "OutlinedDiamond", "Plaid", "Shingle", "SmallCheckerBoard", 
		"SmallConfetti", "SmallGrid", "SolidDiamond", "Sphere", "Trellis", "UpwardDiagonal", "Vertical", 
		"Wave", "Weave", "WideDownwardDiagonal", "WideUpwardDiagonal", "ZigZag"]
	values = [-4105, -4125, -4124, -4124, 18, 15, -4121, -4128, -4162, -4166, 10, 10, 10, 10, 16, 16, 10, 16, 
			15, -4121, -4128, 10, 9, 10, 15, 13, 11, 14, 12, -4128, -4166, 16, 9, 10, 9, 10, 15, 16, 9, 10, -4162, 
			-4166, 10, 10, -4121, -4162, 10]
	d = dict()
	for i in range(len(keys)):
		d[keys[i]] = values[i]
	if key in d:
		return d[key]
	else:
		return None

def GetBevel(key):
	keys = ["None", "Angle", "ArtDeco", "Circle", "Convex", "CoolSlant", "Cross", "Divot", "HardEdge", "RelaxedInset", 
		"Riblet", "Slope", "SoftRound"]
	values = [1, 6, 13, 3, 8, 9, 5, 10, 12, 2, 11, 4, 7]
	d = dict()
	for i in range(len(keys)):
		d[keys[i]] = values[i]
	if key in d:
		return d[key]
	else:
		return None

def RGBToHex(rgb):
	strValue = '%02x%02x%02x' % rgb
	iValue = int(strValue, 16)
	return iValue
"""	
paramList = cellFill.split("~")

patternType = GetPatternType(paramList[0])
bColors = paramList[1].split(",")
backColor = RGBToHex((int(bColors[0]), int(bColors[1]), int(bColors[2])))
fColors = paramList[2].split(",")
foreColor = RGBToHex((int(fColors[0]), int(fColors[1]), int(fColors[2])))
opacity = int(paramList[3])
bevelType = GetBevel(paramList[4])
"""
def LiveStream():
	try:
		xlApp = Marshal.GetActiveObject("Excel.Application")
		xlApp.Visible = True
		xlApp.DisplayAlerts = False
		xlApp.ScreenUpdating = True
		return xlApp
	except:
		return None

def WriteData(ws, data, byColumn, cellFill, borderStyle):
	originX = ws.UsedRange.Row
	originY = ws.UsedRange.Column
	boundX = len(data)
	boundY = len(data[0])
	if byColumn:
		for x in range(0, len(data), 1):
			for y in range(0, len(data[0]), 1):
				ws.Cells[y+1, x+1] = data[x][y]
				if cellFill != None:
					dsColor = cellFill[x][y]
					ws.Cells[y+1, x+1].Interior.Color = RGBToHex((dsColor.Red, dsColor.Green, dsColor.Blue))
				if borderStyle != None:
					ws.Cells[y+1, x+1].BorderAround(GetLineStyle(borderStyle[x][y]))
	else:
		for x in range(0, len(data), 1):
			for y in range(0, len(data[0]), 1):
				ws.Cells[x+1, y+1] = data[x][y]
				if cellFill != None:
					dsColor = cellFill[x][y]
					ws.Cells[x+1, y+1].Interior.Color = RGBToHex((dsColor.Red, dsColor.Green, dsColor.Blue))
				if borderStyle != None:
					ws.Cells[x+1, y+1].BorderAround(GetLineStyle(borderStyle[x][y]))
	return ws

if runMe:
	message = None
	if liveStreaming:
		if LiveStream() == None:
			message = "Please open an Excel session for \nLive Stream mode."
		else:
			xlApp = LiveStream()
			wb = xlApp.ActiveWorkbook
			ws = xlApp.ActiveSheet
			ws.Cells.ClearContents()
			ws.Cells.Clear()
			WriteData(ws, data, byColumn, cellFill, borderStyle)
	else:
		if LiveStream() == None:
			xlApp = Excel.ApplicationClass()
			xlApp.Visible = False
			xlApp.DisplayAlerts = False
			xlApp.ScreenUpdating = False
			if os.path.isfile(str(filePath)):
				xlApp.Workbooks.open(str(filePath))
				wb = xlApp.ActiveWorkbook
				ws = xlApp.Sheets(sheetName)
				ws.Cells.ClearContents()
				ws.Cells.Clear()
			else:
				wb = xlApp.Workbooks.Add()
				ws = wb.Worksheets[1]
			WriteData(ws, data, byColumn, cellFill, borderStyle)
			wb.SaveAs(str(filePath))
			xlApp.ActiveWorkbook.Close(False)
			xlApp.ScreenUpdating = True
			Marshal.ReleaseComObject(ws)
			Marshal.ReleaseComObject(wb)
			Marshal.ReleaseComObject(xlApp)
		else:
			message = "Close currently running Excel \nsession or switch to Live Stream \nmode."
else:
	message = "Run Me is set to False. Please set \nto True if you wish to write data \nto Excel."

#Assign your output to the OUT variable
if message == None:
	OUT = "Success!"
else:
	OUT = '\n'.join('{:^35}'.format(s) for s in message.split('\n'))
