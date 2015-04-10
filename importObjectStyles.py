#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager

# Import RevitAPI
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
catName = IN[0]
nameEquals = IN[1]

gStyles = FilteredElementCollector(doc).OfClass(GraphicsStyle).ToElements()

if nameEquals:
	for i in gStyles:
		if i.GraphicsStyleCategory.Name == str(catName):
			gStyleCategory = i.GraphicsStyleCategory
			break
		else:
			continue
	gStyleSubCategories = gStyleCategory.SubCategories
	gStyleSubCategoriesList = []
	for i in gStyleSubCategories:
		gStyleSubCategoriesList.append(i.Name)
	OUT = gStyleSubCategoriesList
else:
	gStyleCategoryList = []
	for i in gStyles:
		if str(catName) in i.GraphicsStyleCategory.Name:
			gStyleCategoryList.append(i.GraphicsStyleCategory)
	gStyleSubCategories = []
	for i in gStyleCategoryList:
		gStyleSubCategories.append(i.SubCategories)
	gStyleSubCategoriesList = [[] for i in range(0, len(gStyleSubCategories))]
	for index, item in enumerate(gStyleSubCategories):
		for j in item:
			gStyleSubCategoriesList[index].append(j.Name)
	OUT = gStyleSubCategoriesList
