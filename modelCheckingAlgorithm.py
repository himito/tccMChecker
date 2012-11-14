from formula import Formula
from closure import getClosure
from modelCheckingGraph import getAllAtoms, getModelCheckingAtoms, getModelCheckingGraph, searchFormulas, isInAtom
from searchingAlgorithm import getModelCheckingSCCSubgraphs, isSatisfied
from tarjan import tarjan
from PrintGraphs import parserGraphviz

######################################## TCC Structure ########################################

tcc_structure = {	1: {"store": [Formula({"":"in=true"})], "normal": [], "temporal": ["t4","p9"], "edges": [2,3], "initial": True},
					2: {"store": [Formula({"": "x=2"}),Formula({"": "in=true"})], "normal": [], "temporal": ["t4","p9"], "edges": [2,3], "initial": False},
					3: {"store": [Formula({"": "x=2"}),Formula({"~": "in=true"})], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6], "initial": False},
					4: {"store": [Formula({"~": "in=true"})], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6], "initial": True},
					5: {"store": [Formula({"": "x=1"}),Formula({"": "in=true"})], "normal": [], "temporal": ["t4","p9"], "edges": [2,3], "initial": False},
					6: {"store": [Formula({"": "x=1"}),Formula({"~": "in=true"})], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6], "initial": False}
}


######################################## Formula ########################################
phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
print "Formula: "
print phi.getFormula()

######################################## Closure ########################################
closure = []
getClosure(phi,closure)

print "Clausura: ", len(closure)
for formula in closure:
	print formula.getFormula()
	
####################################### Atoms ##########################################
# All atoms	
atoms = getAllAtoms(closure)

# Modecl Checking Atoms
model_checking_atoms = getModelCheckingAtoms(tcc_structure,atoms)

for tcc_node in model_checking_atoms.keys():
	print "Atoms State", tcc_node, "(", len(model_checking_atoms.get(tcc_node)), ")"
	tcc_atoms = model_checking_atoms.get(tcc_node)
	for atom_index in tcc_atoms.keys():
		print "Atom ", atom_index
		for formula in tcc_atoms.get(atom_index):
			print formula.getFormula(), " | ",
		print "\n"

####################################### Model Checking Graph ##########################################
model_checking_graph = getModelCheckingGraph(tcc_structure, model_checking_atoms)
print "Model Checking Graph"
print model_checking_graph

############################## Strongly Connected Components ##########################################
strongly_connected_components = tarjan(model_checking_graph)
print "Strongly Connected Components : "
print strongly_connected_components

model_checking_scc_subgraphs = getModelCheckingSCCSubgraphs(strongly_connected_components, tcc_structure, model_checking_atoms,model_checking_graph)
print "Model Checking SCC Subgraphs (", len(model_checking_scc_subgraphs), ")"
print model_checking_scc_subgraphs


############################## Result ##########################################
result = isSatisfied(phi, tcc_structure, model_checking_atoms, model_checking_scc_subgraphs)
print "Model Satisfies Formula: ", not result

############################# Output ############################################
# parserGraphviz(model_checking_scc_subgraphs[1])


