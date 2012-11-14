# Filename: closure.py

"""
This module contains the functions neccesary to generate the closure of a temporal formula
"""

__author__ = "Jaime E. Arias Almeida"
__license__ = "beerware"
__version__ = "1.0"
__email__ = "jearias@javerianacali.edu.co"
__docformat__ = 'reStructuredText'


from formula import Formula

def getClosure(formula, closure):
	""" 

	Function that generates the closure of a temporal formula.
	
	:param formula: Temporal formula that we want to find the closure 
	:param closure: Empty list to store the subformulas of the closure
	:type formula: Formula
	:type closure: List
	
	:Example:
	
	>>> from closure import *
	>>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
	>>> closure = []
	>>> getClosure(phi,closure)
	>>> for formula in closure:
	...     print formula.getFormula()
	...
	{'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
	{'~': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}
	{'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}
	{'~': {'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}}
	{'o': {'~': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}}
	{'^': {'': 'in=true', '~': {'o': 'x=2'}}}
	{'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
	{'': 'in=true'}
	{'~': 'in=true'}
	{'o': 'x=2'}
	{'~': {'o': 'x=2'}}
	{'o': {'~': 'x=2'}}
	{'': 'x=2'}
	{'~': 'x=2'}
	
	.. note::
	
		This function is based on the conditions shown in the section 6.1 of the thesis document.
	"""

	if formula.isNegativeFormula():
		formula = Formula(formula.getValues())
	
	subformula = formula.getValues()
	
	if formula.isProposition(): # PROPOSITION rule
		closure.append(Formula({"": subformula})) # p
		closure.append(Formula({"~": subformula})) # ~p
	
	elif formula.getConnective() == "^" : # AND rule
		subformulas = formula.getSubFormulas()
		closure.append(Formula({"^": subformula})) # phi ^ psi
		closure.append(Formula({"~": {"^": subformula}})) # ~ (phi ^ psi)
		getClosure(subformulas[0],closure)
		getClosure(subformulas[1],closure)
	
	elif formula.getConnective() == "v" : # OR rule
		subformulas = formula.getSubFormulas()
		closure.append(Formula({"v": subformula})) # phi v psi
		closure.append(Formula({"~": {"v": subformula}})) # ~ (phi v psi)
		getClosure(subformulas[0],closure)
		getClosure(subformulas[1],closure)
		
	elif formula.getConnective() == "o" : # NEXT rule
		closure.append(Formula({"o": subformula})) # o phi
		closure.append(Formula({"~": {"o": subformula}})) # ~o phi
		closure.append(Formula({"o": {"~": subformula}})) # o~ phi
		getClosure(Formula(formula.getValues()),closure)
			
	elif formula.getConnective() == "<>": # FUTURE rule
		closure.append(Formula({"<>": subformula})) # <> phi
		closure.append(Formula({"~": {"<>": subformula}})) # ~<> phi
		closure.append(Formula({"o": {"<>": subformula}})) # o<> phi
		closure.append(Formula({"~": {"o": {"<>": subformula}}})) # ~o<> phi
		closure.append(Formula({"o": {"~": {"<>": subformula}}})) # o~<> phi
		getClosure(Formula(formula.getValues()),closure)

	elif formula.getConnective() == "[]": # GLOBALLY rule
		closure.append(Formula({"[]": subformula})) # [] phi
		closure.append(Formula({"~": {"[]": subformula}})) # ~[] phi
		closure.append(Formula({"o": {"[]": subformula}})) # o[] phi
		closure.append(Formula({"~": {"o": {"[]": subformula}}})) # ~o[] phi
		closure.append(Formula({"o": {"~": {"[]": subformula}}})) # o~[] phi
		getClosure(Formula(formula.getValues()),closure)





