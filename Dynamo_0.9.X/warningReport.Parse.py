# Copyright(c) 2016, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

import os.path
import os

appDataPath = os.getenv('APPDATA')
alPath = appDataPath + r"\Dynamo\0.9\packages\archi-lab.net\extra"
if alPath not in sys.path:
	sys.path.Add(alPath)

from BeautifulSoup import BeautifulSoup
import re

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

file_path = str(IN[0])
err_name = IN[1]
RunIt = IN[2]

if RunIt:
	try:
		errorReport = None
		file = open(file_path, "r")
		err_type, txt4 = [], []
		soup = BeautifulSoup(file)
		tag = soup.findAll('tr')
		for i in tag:
			txt = str(i.text)
			txt2 = txt.rpartition(".")
			txt3 = txt2[0].split(".")
			#Create list of ALL error types in file
			err_type.append(txt3[0])
			#get strings from rows
			txt4.append(str(txt2[-1]))
		#get total number of warnings
		total_warnings = len(err_type)
		#get number of warnings for type specified
		type_warnings = err_type.count(err_name)
		#parse the properties cell for element IDs	
		pattern = re.compile(r"\bid\s*?(\d+)")
		ids = ["; ".join(pattern.findall(item)) for item in txt4]
		#create filtered sets that contain only specified type of error
		err, id = set(), []
		for i, j in zip(err_type, ids):
			if i == err_name:
				err.add(i)
				id.append(j)
		#combine all ids into one string for use with Revit
		final_ids = list(id)
		str_ids = ' ;'.join(str(elem) for elem in final_ids)
		#create a list of individual ids
		list_ids = set(str_ids.replace(" ", "").split(";"))
		output = [err, list_ids, total_warnings, type_warnings]
	except:
		# if error accurs anywhere in the process catch it
		import traceback
		errorReport = traceback.format_exc()
else:
	errorReport = "Set RunIt to True."

#Assign your output to the OUT variable
if errorReport == None:
	OUT = output
else:
	OUT = errorReport
