#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

inputCurves = IN[0]

#join/group curves function
def groupCurves(Line_List): 
	ignore_distance = 0.1 # Assume points this close or closer to each other are touching 
	Grouped_Lines = [] 
	Queue = set() 
	while Line_List: 
		Shape = [] 
		Queue.add(Line_List.pop()) # Move a line from the Line_List to our queue 
		while Queue: 
			Current_Line = Queue.pop() 
			Shape.append(Current_Line) 
			for Potential_Match in Line_List: 
				Points = (Potential_Match.StartPoint, Potential_Match.EndPoint)
				for P1 in Points: 
					for P2 in (Current_Line.StartPoint, Current_Line.EndPoint): 
						distance = P1.DistanceTo(P2) 
						if distance <= ignore_distance: 
							Queue.add(Potential_Match) 
			Line_List = [item for item in Line_List if item not in Queue]
		Grouped_Lines.append(Shape) 
	return Grouped_Lines

OUT = groupCurves(inputCurves)
