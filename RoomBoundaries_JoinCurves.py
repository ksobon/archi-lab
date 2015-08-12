import clr
import sys
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

from System import Array
from System.Collections.Generic import *

walls = IN[0]
curves = IN[1]


for i, (wList, cList) in enumerate(zip(walls, curves)):
	for j, (wall, curve) in enumerate(zip(wList, cList)):
		if wall == None:
			del walls[i][j]
			# take corresponding curve and join it to next one in order
			# if there is no next one, then use previous
			curveList = [curves[i][j], curves[i][j+1]]
			curveArray = List[Curve](curveList)
			newPolyCurve = PolyCurve.ByJoinedCurves(curveArray)
			curves[i][j+1] = newPolyCurve
			del curves[i][j]

OUT = [walls, curves]
