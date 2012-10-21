# -*- coding: utf-8 -*-
from formula import Formula
from closure import getClosure

tcc_structure = {	1: {"store": [{"":"in=true"}], "normal": [], "temporal": ["t4","p9"], "edges": [2,3]},
					2: {"store": [{"": "x=2"},{"": "in=true"}], "normal": [], "temporal": ["t4","p9"], "edges": [2,3]},
					3: {"store": [{"": "x=2"},{"~": "in=true"}], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6]},
					4: {"store": [{"~": "in=true"}], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6]},
					5: {"store": [{"": "x=1"},{"": "in=true"}], "normal": [], "temporal": ["t4","p9"], "edges": [2,3]},
					6: {"store": [{"": "x=1"},{"~": "in=true"}], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6]}
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

def searchFormulas(formulas, connective):
	result = []
	for formula in formulas:
		if formula.getConnective() == connective:
			result.append(formula)
	return result

def getAllAtoms(basicFormulas):
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
	
	return atoms


# Basic Formulas
basicFormulas = getBasicFormulas(closure)
print "Basic Formulas"
for formula in basicFormulas:
	print formula.formula


# All Atoms
atoms = getAllAtoms(basicFormulas)
print "Atoms: ", len(atoms)
for atom in atoms:
	for formula in atom:
		print formula.formula, " | ",
	print "\n"


print "Nueva closure:"

for formula in closure:
	if formula.getConnective() != "~" and formula.getConnective() != "o" and not formula.isProposition():
		print formula.formula	
	
	




# tcc_node = 1
# atom = []
# propositions = tcc_structure.get(tcc_node).get("store")
# for proposition in propositions: # Propositions as formulas
# 	atom.append(Formula(proposition))
