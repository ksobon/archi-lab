#Copyright(c) 2015, Konrad Sobon
#@arch_laboratory, http://archi-lab.net

# Default imports
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#The input to this node will be stored in the IN[0] variable.
dataEnteringNode = IN[0]

sequence = IN[0]
uniq_seq = []

def increment_item(item = 'A'):
    next_char = [ord(char) for char in item]
    next_char[-1] += 1
    for index in xrange(len(next_char)-1, -1, -1):
            if next_char[index] > ord('Z'):
                    next_char[index] = ord('A')
                    if index > 0:
                            next_char[index-1] += 1
                    else:
                            next_char.append(ord('A'))
    return ''.join((chr(char) for char in next_char))

def char_generator(start = 'A'):
    current = start
    yield start
    while True:
        current = increment_item(current)
        yield current

def build_unique_sequence(sequence):
    key_set = dict([item, char_generator()] for item in set(sequence))
    return map(lambda item:'{}{}'.format(item, key_set[item].next()), sequence)
    
OUT = build_unique_sequence(sequence)
