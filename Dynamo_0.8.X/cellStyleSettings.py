# Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

# Import RevitAPI
import clr
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import System
from System.Collections.Generic import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import System

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

_backgroundColor = IN[0]
_bold = IN[1]
_font = IN[2]
_fontColor = IN[3]
_fontSize = IN[4]
_italics = IN[5]
_underline = IN[6]
_orientation = IN[7]
_hAlign = IN[8]
_vAlign = IN[9]
_headerText = IN[10]

_borderBottom = IN[11]
_borderLeft = IN[12]
_borderRight = IN[13]
_borderTop = IN[14]


#design script color to RVT color function
def dsColorToRvtColor(dsColor):
	R = dsColor.Red
	G = dsColor.Green
	B = dsColor.Blue
	return Autodesk.Revit.DB.Color(R,G,B)

try:
	errorReport = None	
	options = TableCellStyleOverrideOptions()
	
	if _backgroundColor != None:
		options.BackgroundColor = True
	if _bold != None:
		options.Bold = True
	
	borderOptions = [_borderBottom, _borderLeft, _borderRight, _borderTop]
	if any(item != None for item in borderOptions):
		options.BorderLineStyle = True
	
	if _borderBottom != None:
		options.BorderBottomLineStyle = True
	if _borderLeft != None:
		options.BorderLeftLineStyle = True
	if _borderRight != None:
		options.BorderRightLineStyle = True
	if _borderTop != None:
		options.BorderTopLineStyle = True
	
	if _font != None:
		options.Font = True
	if _fontColor != None:
		options.FontColor = True
	if _fontSize != None:
		options.FontSize = True
	if _italics != None:
		options.Italics = True
	if _underline != None:
		options.Underline = True
	if _orientation != None:
		options.TextOrientation = True
	
	if _hAlign != None:
		options.HorizontalAlignment = True
	if _vAlign != None:
		options.VerticalAlignment = True
	
	tcs = TableCellStyle()
	tcs.SetCellStyleOverrideOptions(options)
	
	if _backgroundColor != None:
		tcs.BackgroundColor = dsColorToRvtColor(_backgroundColor)
	if _bold != None:
		tcs.IsFontBold = _bold
	
	if _borderBottom != None:
		tcs.BorderBottomLineStyle = UnwrapElement(_borderBottom).GraphicsStyleCategory.Id
	if _borderLeft != None:
		tcs.BorderLeftLineStyle = UnwrapElement(_borderLeft).GraphicsStyleCategory.Id
	if _borderRight != None:
		tcs.BorderRightLineStyle = UnwrapElement(_borderRight).GraphicsStyleCategory.Id
	if _borderTop != None:
		tcs.BorderTopLineStyle = UnwrapElement(_borderTop).GraphicsStyleCategory.Id
	
	if _font != None:
		tcs.FontName = _font
	if _fontColor != None:
		tcs.TextColor = dsColorToRvtColor(_fontColor)
	if _fontSize != None:
		tcs.TextSize = _fontSize
	if _italics != None:
		tcs.IsFontItalic  = _italics
	if _underline != None:
		tcs.IsFontUnderline  = _underline
	if _orientation != None:
		tcs.TextOrientation = _orientation
	
	if _hAlign != None:
		tcs.FontHorizontalAlignment = System.Enum.Parse(Autodesk.Revit.DB.HorizontalAlignmentStyle, _hAlign)
	if _vAlign != None:
		tcs.FontVerticalAlignment = System.Enum.Parse(Autodesk.Revit.DB.VerticalAlignmentStyle, _vAlign)
	
	_headerOut = [tcs, _headerText]

except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = _headerOut
else:
	OUT = errorReport
