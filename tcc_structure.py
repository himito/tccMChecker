# -*- coding: utf-8 -*-
from formula import Formula
from closure import getClosure

tcc_structure = {	1: {"store": [Formula({"":"in=true"})], "normal": [], "temporal": ["t4","p9"], "edges": [2,3]},
					2: {"store": [Formula({"": "x=2"}),Formula({"": "in=true"})], "normal": [], "temporal": ["t4","p9"], "edges": [2,3]},
					3: {"store": [Formula({"": "x=2"}),Formula({"~": "in=true"})], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6]},
					4: {"store": [Formula({"~": "in=true"})], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6]},
					5: {"store": [Formula({"": "x=1"}),Formula({"": "in=true"})], "normal": [], "temporal": ["t4","p9"], "edges": [2,3]},
					6: {"store": [Formula({"": "x=1"}),Formula({"~": "in=true"})], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6]}
}


######################################## Formula ########################################
phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
print "Formula: "
print phi.formula

######################################## Closure ########################################
closure = []
getClosure(phi,closure)

print "Clausura: ", len(closure)
for formula in closure:
	print formula.formula


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


# Basic Formulas
basicFormulas = getBasicFormulas(closure)
print "Basic Formulas"
for formula in basicFormulas:
	print formula.formula

# No Basic Formulas
noBasicFormulas = getNoBasicFormulas(closure)
print "Nueva closure:"
for formula in noBasicFormulas:
	print formula.formula
	

# All Atoms

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

atoms = getAllAtoms(basicFormulas, noBasicFormulas)


# print "Atoms: ", len(atoms)
# for atom in atoms:
# 	for formula in atom:
# 		print formula.formula, " | ",
# 	print "\n"

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
		model_checking_atoms[tcc_node] = atoms_node
	return model_checking_atoms


model_checking_atoms = getModelCheckingAtoms(tcc_structure,atoms)


for tcc_node in model_checking_atoms.keys():
	print "Atoms State", tcc_node, "(", len(model_checking_atoms.get(tcc_node)), ")"

	for atom in model_checking_atoms.get(tcc_node):
		for formula in atom:
			print formula.formula, " | ",
		print "\n"