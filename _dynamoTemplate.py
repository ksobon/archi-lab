# Copyright(c) 2017, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr

clr.AddReference('ProtoGeometry')
import Autodesk.DesignScript.Geometry

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit

clr.ImportExtensions(Revit.Elements)

# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Import RevitAPI
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

import System
from System import Array
from System.Collections.Generic import *

import sys

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)


def process_list(_func, _list):
    return map(lambda x: process_list(_func, x) if type(x) == list else _func(x), _list)


def process_list_arg(_func, _list, _arg):
    return map(lambda x: process_list_arg(_func, x, _arg) if type(x) == list else _func(x, _arg), _list)


def process_parallel_lists(_func, *lists):
    return map(lambda *xs: process_parallel_lists(_func, *xs) if all(type(x) is list for x in xs) else _func(*xs),
               *lists)


def to_list(x):
    if hasattr(x, '__iter__'):
        return x
    else:
        return [x]


# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)
# Regenerate
TransactionManager.Instance.ForceCloseTransaction()

try:
    errorReport = None

except:
    # if error occurs anywhere in the process catch it
    import traceback

    errorReport = traceback.format_exc()

# End Transaction
TransactionManager.Instance.TransactionTaskDone()

# Assign your output to the OUT variable
if None == errorReport:
    OUT = 0
else:
    OUT = errorReport
