# Filename: modelCheckingGraph.py

"""
This module contains the necessary functions to generate a model checking graph.
"""

__author__ = "Jaime E. Arias Almeida"
__license__ = "beerware"
__version__ = "1.0"
__email__ = "jearias@javerianacali.edu.co"
__docformat__ = 'reStructuredText'

from formula import Formula

######################################## Atoms ########################################
def getBasicFormulas(closure):
	"""
		Returns the basic formulas (i.e. propositions or formulas with :math:`\circ` as main connective) of the closure.

		:param closure: Closure of a formula.
		:type closure: List of :py:class:`~formula.Formula`

		:returns: List of basic formulas of the closure.
		:rtype: List of :py:class:`~formula.Formula`.

		:Example:

		>>> from closure import *
		>>> from modelCheckingGraph import *
		>>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
		>>> closure = []
		>>> getClosure(phi,closure)
		>>> basicFormulas = getBasicFormulas(closure)
		>>> for formula in basicFormulas:
		...     print formula.getFormula()
		... 
		{'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}
		{'': 'in=true'}
		{'o': 'x=2'}
		{'': 'x=2'}

		.. seealso::
			:py:func:`closure.getClosure`

	"""
	basicFormulas = []
	for formula in closure:
		if formula.isBasic():
			basicFormulas.append(formula)
	return basicFormulas

def getNoBasicFormulas(closure):
	"""
		Returns the formulas of the closure that are not basic formulas.
		
		:param closure: Closure of a formula.
		:type closure: List of :py:class:`~formula.Formula`
		
		:returns: List of formulas of the closure that are not basic formulas.
		:rtype: List of :py:class:`~formula.Formula`.
		
		:Example:
		
		>>> from closure import *
		>>> from modelCheckingGraph import *
		>>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
		>>> closure = []
		>>> getClosure(phi,closure)
		>>> noBasicFormulas = getNoBasicFormulas(closure)
		>>> for formula in noBasicFormulas:
		...     print formula.getFormula()
		... 
		{'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
		{'^': {'': 'in=true', '~': {'o': 'x=2'}}}
		
		.. seealso::
			:py:func:`closure.getClosure`
		
	"""
	result = []
	for formula in closure:
		if formula.getConnective() != "~" and formula.getConnective() != "o" and not formula.isProposition():
			result.append(formula)
	return result
	

def searchFormulas(formulas, connective):
	"""
		Returns the formulas that have a particular main connective.
		
		:param formulas: List of formulas.
		:type formulas: List of :py:class:`~formula.Formula`
		
		:param connective: The main connective.
		:type connective: String
		
		:returns: List containing the formulas that have the main connective.
		:rtype: List
		
		:Example:
		
		>>> from modelCheckingGraph import *
		>>> list = [Formula({'o': 'x=2'}), Formula({'~': {'o': 'x=2'}}), Formula({'o': {'~': 'x=2'}})]
		>>> result = searchFormulas(list,'o')
		>>> for formula in result:
		...     print formula.getFormula()
		... 
		{'o': 'x=2'}
		{'o': {'~': 'x=2'}}
		
	"""
	result = []
	for formula in formulas:
		if formula.getConnective() == connective:
			result.append(formula)
	return result

def getAllAtoms(closure):
	"""
		Returns all possible atoms of the closure.
		
		:param closure: Closure of a formula.
		:type closure: List of :py:class:`~formula.Formula`
		
		:returns: List of all atoms of the closure.
		:rtype: List of lists of :py:class:`~formula.Formula`.
		
		:Example:
		
		>>> from closure import *
		>>> from modelCheckingGraph import *
		>>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
		>>> closure = []
		>>> getClosure(phi,closure)
		>>> atoms = getAllAtoms(closure)
		>>> for index, atom in enumerate(atoms):
		...     print "Atom " + str(index) + ":"
		...     for formula in atom:
		...             print formula.getFormula()
		... 
		Atom 0:
		{'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}
		{'': 'in=true'}
		{'o': 'x=2'}
		{'': 'x=2'}
		{'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
		{'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
		Atom 1:
		{'~': {'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}}
		{'': 'in=true'}
		{'o': 'x=2'}
		{'': 'x=2'}
		{'o': {'~': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}}
		{'~': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}
		{'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
		...
		
		.. seealso::
			:py:func:`closure.getClosure`
		
		.. note::
		
			This function is based on the algorithm shown in [MP95]_.
		
	"""
	basicFormulas = getBasicFormulas(closure)
	noBasicFormulas = getNoBasicFormulas(closure)
	num_atoms = 2**len(basicFormulas)
	atoms =  [ [] for i in range(num_atoms) ]

	# 2^b Combinations
	for index_basic_formula in range(len(basicFormulas)):
		num = 2** index_basic_formula
		index_negative = 0
		negative = False
		for index in range(num_atoms):
			if index_negative == num:
				negative = not(negative)
				index_negative = 0
			if negative:
				atoms[index].append(basicFormulas[index_basic_formula].getNegation())
			else:
				atoms[index].append(basicFormulas[index_basic_formula])
			index_negative += 1
		
	# o~phi
	f_temps = searchFormulas(basicFormulas,"o")
	for formula in f_temps:
		for atom in atoms:
			if formula not in atom:
				atom.append(Formula({"o":{"~": formula.getValues()}}))
	
	for formula in noBasicFormulas:
		for atom in atoms:
			if isConsistent(formula, atom):
				atom.append(formula)
			else: 
				atom.append(formula.getNegation())
	
	return atoms

def isInAtom(formula, atom):
	"""
		Checks if a formula is in an atom.
		
		:param formula: Structure representing a formula.
		:type formula: Dictionary
		
		:param atom: List of consistent formulas representing an atom of the closure.
		:type atom: List of :py:class:`~formula.Formula`.
		
		:returns: ``True`` if the formula is in atom or ``False`` otherwise.
		:rtype: Boolean
		
		:Example:
		
		>>> from closure import *
		>>> from modelCheckingGraph import *
		>>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
		>>> closure = []
		>>> getClosure(phi,closure)
		>>> atoms = getAllAtoms(closure)
		>>> isInAtom({'': 'in=true'}, atoms[0])
		True
	"""
	for formulaAtom in atom:
		# print "comparar:" , formula , " con: ", formulaAtom.formula
		if formulaAtom.getFormula() == formula:
			return True
	return False


def isConsistent(formula, atom):
	"""
		Checks if a formula is consistent with the set of formulas in an atom.
		
		:param formula: Formula 
		:type formula: :py:class:`~formula.Formula`
		
		:param atom: List of consistent formulas representing an atom of the closure.
		:type atom: List of :py:class:`~formula.Formula`.
		
		:returns: ``True`` if the formula is consistent with the set of formulas in the atom or ``False`` otherwise.
		:rtype: Boolean
		
		:Example:
		
		>>> from closure import *
		>>> from modelCheckingGraph import *
		>>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
		>>> closure = []
		>>> getClosure(phi,closure)
		>>> atoms = getAllAtoms(closure)
		>>> isConsistent(Formula({'': 'x=1'}), atoms[0])
		False
		
		
		.. note::
		
			This function is based on the conditions shown in the defintion 6.1 of the thesis document.
	"""
	rules = {"x=2": Formula({"~": "x=1"}), "x=1": Formula({"~": "x=2"})}
	# print formula.formula
	if not isInAtom(formula.getNegation().getFormula(), atom):
		if formula.getConnective() == "<>": # <> rules
			if isInAtom({"o": formula.getFormula()},atom) or isConsistent(Formula(formula.getValues()), atom):
				return True
		elif formula.getConnective() == "[]": # [] rules
			if isInAtom({"o": formula.getFormula()},atom) and isConsistent(Formula(formula.getValues()), atom):
				return True
		elif formula.getConnective() == "^": # ^ rules
			subformulas = formula.getSubFormulas()
			if isConsistent(subformulas[0], atom) and isConsistent(subformulas[1], atom):
				return True
		elif formula.getConnective() == "v": # v rules
			subformulas = formula.getSubFormulas()
			if isConsistent(subformulas[0], atom) or isConsistent(subformulas[1], atom):
				return True
		elif formula.isProposition() or formula.getConnective() == "o" or formula.isNegativeNext():
			if isInAtom(formula.getFormula(), atom):
				return True
	return False



######################################## Atoms  for tcc nodes ########################################

def __deleteAtoms(atoms, index_list):
	result = []
	index = 0
	while index < len(atoms):
		if index in index_list:
			result.insert(0,atoms[index])
		else:
			result.append(atoms[index])
		index +=1
	return result[len(index_list):]

def propositionConsistent(formula, atom):
	if formula.isProposition() and (formula.getValues() in formula.getPropositionRules().keys()):
		if isConsistent(Formula(formula.getConsistentPropositions()), atom):
			return True
	return False
	
def __list2dict(lists, offset):
	result = {}
	for index, element in enumerate(lists):
	    result[index+offset] = element
	return result

def __getTotalNodes(graph):
	total = 0
	for index_node in graph.keys():
		total = total + len(graph.get(index_node))
	return total
	
def getModelCheckingAtoms(tcc_structure, atoms):
	model_checking_atoms = {}
	for tcc_node in tcc_structure.keys():
		atoms_node = atoms
		propositions = tcc_structure.get(tcc_node).get("store")
		for proposition in propositions: # Propositions as formulas
			index_atom = 0
			delete_atoms = []
			while index_atom < len(atoms_node):
				atom = atoms_node[index_atom]
		
				if  isConsistent(proposition,atom) or propositionConsistent(proposition, atom):
					if not isInAtom(proposition.getFormula(),atom):
						atoms_node[index_atom].append(proposition)
				else:
					delete_atoms.append(index_atom)
				index_atom +=1
			atoms_node = __deleteAtoms(atoms_node,delete_atoms)
		model_checking_atoms[tcc_node] = __list2dict(atoms_node,__getTotalNodes(model_checking_atoms) + 1)
	return model_checking_atoms
	
######################################## Model Checking Graph ########################################

def isNextState(nextFormulas,nextAtom):
	for formula in nextFormulas:
		next = Formula(formula.getValues())
		if not isInAtom(next.getFormula(), nextAtom): 
			return False
	return True

def getModelCheckingGraph(tcc_structure, model_checking_atoms):
	model_checking_graph={}
	for tcc_node in tcc_structure.keys():
		atoms_tcc_node = model_checking_atoms.get(tcc_node)
		for index_n1 in atoms_tcc_node.keys():
			atom_n1  = atoms_tcc_node.get(index_n1)
			nextFormulas = searchFormulas(atom_n1,"o")
			next_nodes = []
			for next_tcc_node in tcc_structure[tcc_node].get("edges"):
				atoms_next_tcc_node = model_checking_atoms.get(next_tcc_node)
				for index_n2 in atoms_next_tcc_node.keys():
					atom_n2 = atoms_next_tcc_node.get(index_n2)
					if isNextState(nextFormulas, atom_n2):
						print "tcc state: ", tcc_node, "(", index_n1, ") -> ", "next tcc state", next_tcc_node, "(", index_n2, ")"
						next_nodes.append(index_n2)
			model_checking_graph[index_n1] = next_nodes
	return model_checking_graph









