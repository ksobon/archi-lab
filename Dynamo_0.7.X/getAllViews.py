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

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

from System.Collections.Generic import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

#collect all views in the model
collector = FilteredElementCollector(doc)
views = collector.OfClass(View).ToElements()

#sort views into separate lists based on view type
areaPlans, ceilingPlans, columnSchedules = [], [], []
costReport, details, draftingViews = [], [], []
drawingSheets, elevations, engineetingPlans = [], [], []
floorPlans, internal, legends, loadReports = [], [], [], []
panelSchedules, pressureLossReports, renderings = [], [], []
reports, schedules, sections, threeD = [], [], [], []
undefined, walkthrough = [], []
for i in views:
	if not i.IsTemplate:
		if i.ViewType == ViewType.AreaPlan:
			areaPlans.append(i.ToDSType(True))
		elif i.ViewType == ViewType.CeilingPlan:
			ceilingPlans.append(i.ToDSType(True))
		elif i.ViewType == ViewType.ColumnSchedule:
			columnSchedules.append(i.ToDSType(True))
		elif i.ViewType == ViewType.CostReport:
			costReport.append(i.ToDSType(True))
		elif i.ViewType == ViewType.Detail:
			details.append(i.ToDSType(True))
		elif i.ViewType == ViewType.DraftingView:
			draftingViews.append(i.ToDSType(True))
		elif i.ViewType == ViewType.DrawingSheet:
			drawingSheets.append(i.ToDSType(True))
		elif i.ViewType == ViewType.Elevation:
			elevations.append(i.ToDSType(True))
		elif i.ViewType == ViewType.EngineeringPlan:
			engineetingPlans.append(i.ToDSType(True))
		elif i.ViewType == ViewType.FloorPlan:
			floorPlans.append(i.ToDSType(True))
		elif i.ViewType == ViewType.Internal:
			internal.append(i.ToDSType(True))
		elif i.ViewType == ViewType.Legend:
			legends.append(i.ToDSType(True))
		elif i.ViewType == ViewType.LoadsReport:
			loadReports.append(i.ToDSType(True))
		elif i.ViewType == ViewType.PanelSchedule:
			panelSchedules.append(i.ToDSType(True))
		elif i.ViewType == ViewType.PresureLossReport:
			pressureLossReports.append(i.ToDSType(True))
		elif i.ViewType == ViewType.Rendering:
			renderings.append(i.ToDSType(True))
		elif i.ViewType == ViewType.Report:
			reports.append(i.ToDSType(True))
		elif i.ViewType == ViewType.Schedule:
			schedules.append(i.ToDSType(True))
		elif i.ViewType == ViewType.Section:
			sections.append(i.ToDSType(True))
		elif i.ViewType == ViewType.ThreeD:
			threeD.append(i.ToDSType(True))
		elif i.ViewType == ViewType.Undefined:
			undefined.append(i.ToDSType(True))
		elif i.ViewType == ViewType.Walkthrough:
			walkthrough.append(i.ToDSType(True))
		else:
			continue

#Assign your output to the OUT variable
OUT = areaPlans, ceilingPlans, columnSchedules, costReport, \
	details, draftingViews, drawingSheets, elevations, \
	engineetingPlans, floorPlans, internal, legends, \
	loadReports, panelSchedules, pressureLossReports, \
	renderings, reports, schedules, sections, threeD, \
	undefined, walkthrough
