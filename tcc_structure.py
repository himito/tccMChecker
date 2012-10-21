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
def getBasicFormulas(closure):
	basicFormulas = []
	for formula in closure:
		if formula.isBasic():
			basicFormulas.append(formula)
	return basicFormulas


closure = []
getClosure(phi,closure)
basicFormulas = getBasicFormulas(closure)

print "Clausura: ", len(closure)
for formula in closure:
	print formula.formula

print "Basic Formulas"
for formula in basicFormulas:
	print formula.formula

######################################## Atoms ########################################

num_atoms = 2**len(basicFormulas)
atoms =  [ [] for i in range(num_atoms) ]
print "Atoms: ", num_atoms
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

for atom in atoms:
	for formula in atom:
		print formula.formula, " | ",
	print "\n"



# tcc_node = 1
# atom = []
# propositions = tcc_structure.get(tcc_node).get("store")
# for proposition in propositions: # Propositions as formulas
# 	atom.append(Formula(proposition))


# print "Atoms:"
# for formula in atom:
# 	print formula.formula