#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

# This bit of code was a great work by Stack Overflow user: wdscxsj
# The original thread can be found here: http://stackoverflow.com/questions/10109030/is-it-possible-to-get-a-list-of-printer-names-in-windows/10109522?noredirect=1#comment50322136_10109522

# Use EnumPrintersW to list local printers with their names and descriptions.
# Tested with CPython 2.7.10 and IronPython 2.7.5.

import ctypes
from ctypes.wintypes import BYTE, DWORD, LPCWSTR

winspool = ctypes.WinDLL('winspool.drv')  # for EnumPrintersW
msvcrt = ctypes.cdll.msvcrt  # for malloc, free

# Parameters: modify as you need. See MSDN for detail.
PRINTER_ENUM_LOCAL = 2
Name = None  # ignored for PRINTER_ENUM_LOCAL
Level = 1  # or 2, 4, 5

class PRINTER_INFO_1(ctypes.Structure):
	_fields_ = [
		("Flags", DWORD),
		("pDescription", LPCWSTR),
		("pName", LPCWSTR),
		("pComment", LPCWSTR),
	]

# Invoke once with a NULL pointer to get buffer size.
info = ctypes.POINTER(BYTE)()
pcbNeeded = DWORD(0)
pcReturned = DWORD(0)  # the number of PRINTER_INFO_1 structures retrieved
winspool.EnumPrintersW(PRINTER_ENUM_LOCAL, Name, Level, ctypes.byref(info), 0, ctypes.byref(pcbNeeded), ctypes.byref(pcReturned))

bufsize = pcbNeeded.value
buffer = msvcrt.malloc(bufsize)
winspool.EnumPrintersW(PRINTER_ENUM_LOCAL, Name, Level, buffer, bufsize, ctypes.byref(pcbNeeded), ctypes.byref(pcReturned))
info = ctypes.cast(buffer, ctypes.POINTER(PRINTER_INFO_1))

printerNames = []
for i in range(pcReturned.value):
	printerNames.append(info[i].pName)
msvcrt.free(buffer)

#Assign your output to the OUT variable
OUT = printerNames
