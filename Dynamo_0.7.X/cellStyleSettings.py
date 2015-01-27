#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

_backgroundColor = IN[0]
_bold = IN[1]
""" to be added when I figure out how to actually make it work :-)
_borderBottom = IN[2]
_borderLeft = IN[3]
_borderRight = IN[4]
_borderTop = IN[5]
"""
_font = IN[2]
_fontColor = IN[3]
_fontSize = IN[4]
_italics = IN[5]
_underline = IN[6]
_orientation = IN[7]

_hAlign = IN[8]
_vAlign = IN[9]

_headerText = IN[10]

#design script color to RVT color function
def dsColorToRvtColor(dsColor):
	R = dsColor.Red
	G = dsColor.Green
	B = dsColor.Blue
	return Autodesk.Revit.DB.Color(R,G,B)

options = TableCellStyleOverrideOptions()

if _backgroundColor != None:
	options.BackgroundColor = True
if _bold != None:
	options.Bold = True
"""
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
"""
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
"""
if _borderBottom != None:
	tcs.BorderBottomLineStyle = UnwrapElement(_borderBottom).Id
if _borderLeft != None:
	tcs.BorderLeftLineStyle = UnwrapElement(_borderLeft).Id
if _borderRight != None:
	tcs.BorderRightLineStyle = UnwrapElement(_borderRight).Id
if _borderTop != None:
	tcs.BorderTopLineStyle = UnwrapElement(_borderTop).Id
"""
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
	if _hAlign == "Left":
		has = HorizontalAlignmentStyle.Left
	elif _hAlign == "Center":
		has = HorizontalAlignmentStyle.Center
	elif _hAlign == "Right":
		has = HorizontalAlignmentStyle.Right
	tcs.FontHorizontalAlignment = has
if _vAlign != None:
	if _vAlign == "Top":
		vas = VerticalAlignmentStyle.Top
	elif _vAlign == "Middle":
		vas = VerticalAlignmentStyle.Middle
	elif _vAlign == "Bottom":
		vas = VerticalAlignmentStyle.Bottom
	tcs.FontVerticalAlignment = vas

_headerOut = [tcs, _headerText]
#Assign your output to the OUT variable
OUT = _headerOut
