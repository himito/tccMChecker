# -*- coding: utf-8 -*-
from formula import Formula

######################################## Atoms ########################################
def getBasicFormulas(closure):
	basicFormulas = []
	for formula in closure:
		if formula.isBasic():
			basicFormulas.append(formula)
	return basicFormulas

def getNoBasicFormulas(closure):
	result = []
	for formula in closure:
		if formula.getConnective() != "~" and formula.getConnective() != "o" and not formula.isProposition():
			result.append(formula)
	return result
	

def searchFormulas(formulas, connective):
	result = []
	for formula in formulas:
		if formula.getConnective() == connective:
			result.append(formula)
	return result

def getAllAtoms(basicFormulas, noBasicFormulas):
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
	for formulaAtom in atom:
		if formulaAtom.formula == formula:
			return True
	return False


def isConsistent(formula, atom):
	rules = {"x=2": Formula({"~": "x=1"}), "x=1": Formula({"~": "x=2"})}
	# print formula.formula
	if not isInAtom(formula.getNegation().formula, atom):
		if formula.getConnective() == "<>": # <> rules
			if isInAtom({"o": formula.formula},atom) or isConsistent(Formula(formula.getValues()), atom):
				return True
		elif formula.getConnective() == "[]": # [] rules
			if isInAtom({"o": formula.formula},atom) and isConsistent(Formula(formula.getValues()), atom):
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
			if isInAtom(formula.formula, atom):
				return True
	return False



######################################## Atoms  for tcc nodes ########################################

def deleteAtoms(atoms, index_list):
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
	if formula.isProposition() and (formula.getValues() in formula.proposition_rules.keys()):
		if isConsistent(Formula(formula.getPropositionConsistent()), atom):
			return True
	return False
def list2dict(lists, offset):
	result = {}
	for index, element in enumerate(lists):
	    result[index+offset] = element
	return result

def getTotalNodes(graph):
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
					if not isInAtom(proposition.formula,atom):
						atoms_node[index_atom].append(proposition)
				else:
					delete_atoms.append(index_atom)
				index_atom +=1
			atoms_node = deleteAtoms(atoms_node,delete_atoms)
		model_checking_atoms[tcc_node] = list2dict(atoms_node,getTotalNodes(model_checking_atoms) + 1)
	return model_checking_atoms
	
######################################## Model Checking Graph ########################################

def isNextState(nextFormulas,nextAtom):
	for formula in nextFormulas:
		next = Formula(formula.getValues())
		if not isInAtom(next.formula, nextAtom): 
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









