import clr
import sys
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

import string
import re

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

cellAddress = str(IN[0])
sheet = IN[1]

def ConvertNumber(num):
	letters = ''
	while num:
		mod = num % 26
		num = num // 26
		letters += chr(mod + 64)
	return ''.join(reversed(letters))

def ConvertChar(char):
	number =- 25
	for l in char:
		if not l in string.ascii_letters:
			return False
		number += ord(l.upper()) - 64 + 25
	return number

match = re.match(r"([a-z]+)([0-9]+)", cellAddress, re.I)
if match:
    addressItems = match.groups()

row = ConvertChar(addressItems[0])
column = int(addressItems[1])

if sheet == None:
	sheet = 0
	
#Assign your output to the OUT variable
OUT = row, column, sheet
