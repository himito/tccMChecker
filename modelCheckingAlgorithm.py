from formula import Formula
from closure import getClosure
from modelCheckingGraph import getBasicFormulas, getNoBasicFormulas, getAllAtoms, getModelCheckingAtoms, getModelCheckingGraph
from tarjan import tarjan

######################################## TCC Structure ########################################

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
	
####################################### Atoms ##########################################
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

# All atoms	
atoms = getAllAtoms(basicFormulas, noBasicFormulas)

# Modecl Checking Atoms
model_checking_atoms = getModelCheckingAtoms(tcc_structure,atoms)

for tcc_node in model_checking_atoms.keys():
	print "Atoms State", tcc_node, "(", len(model_checking_atoms.get(tcc_node)), ")"
	tcc_atoms = model_checking_atoms.get(tcc_node)
	for atom_index in tcc_atoms.keys():
		print "Atom ", atom_index
		for formula in tcc_atoms.get(atom_index):
			print formula.formula, " | ",
		print "\n"

####################################### Model Checking Graph ##########################################
model_checking_graph = getModelCheckingGraph(tcc_structure, model_checking_atoms)

############################## Strongly Connected Components ##########################################
strongly_connected_components = tarjan(model_checking_graph)
print strongly_connected_components








