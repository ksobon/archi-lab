#Copyright(c) 2016, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

inputListTrue = IN[0]
inputListFalse = IN[1]
pattern = IN[2]
result = []

def choose(first, second, value):
    if hasattr(first, '__iter__'):
        return [choose(i,j,k) for i,j,k in zip(first, second, value)]
    else:
        return first if value else second

OUT = choose(inputListTrue, inputListFalse, pattern)
