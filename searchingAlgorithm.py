import itertools
from formula import Formula
from modelCheckingGraph import searchFormulas, isInAtom


def getInitialNodes(tcc_structure,model_checking_atoms):
	initial_nodes = []
	for node in tcc_structure.keys():
		if tcc_structure.get(node).get("initial"):
			initial_nodes.append(model_checking_atoms.get(node).keys())
	return list(itertools.chain(*initial_nodes))
		

def getModelCheckingSCCSubgraphs(scc_list,tcc_structure,model_checking_atoms,model_checking_graph):
	initial_nodes = getInitialNodes(tcc_structure,model_checking_atoms)
	model_checking_subgraphs=[]
	for scc in scc_list :
		if len(scc) > 1:  # non-trivial
			temp_graph = {}
			for nodo in scc:
				nodes =  list(set(model_checking_graph.get(nodo)).intersection(set(scc)))
				if len(nodes) != 0:
					temp_graph[nodo] = nodes
			for nodo in initial_nodes:
				nodes = list(set(model_checking_graph.get(nodo)).intersection(set(scc)))
				if len(nodes) != 0:
					temp_graph[nodo] = nodes
			model_checking_subgraphs.append(temp_graph)
	return model_checking_subgraphs
	
def getFormulas(node,model_checking_atoms):
	for tcc_node in model_checking_atoms.keys():
		if node in model_checking_atoms.get(tcc_node).keys():
			return model_checking_atoms[tcc_node].get(node)


def isSelfFulfilling(scc_graph, initial_nodes, model_checking_atoms):
	for node in scc_graph.keys():
		if node not in initial_nodes:
			formulas = getFormulas(node,model_checking_atoms)
			diamond_formulas = searchFormulas(formulas, "<>")

			for diamond_formula in diamond_formulas:
				new_formula = Formula(diamond_formula.getValues())

				print "search de node:", node,
				print new_formula.formula

				found = False
				for node_scc in scc_graph.keys():
					if node_scc not in initial_nodes:

						print "en node: ", node_scc

						formulas_scc = getFormulas(node_scc, model_checking_atoms)
						# for formula in formulas_scc:
						# 	print formula.formula, "|"

						print "Encontrado:", isInAtom(new_formula.formula, formulas_scc)
						if isInAtom(new_formula.formula, formulas_scc):
							found = True
							break
				if not found:
					return False
	return True


def initialNodesEntailFormula(scc_graph, initial_nodes, model_checking_atoms,formula):
	print "Formula:", formula.formula
	for node in scc_graph.keys():
		if node in initial_nodes:
			formulas = getFormulas(node,model_checking_atoms)
			print "node:", node
			print "Entails:", isInAtom(formula.formula, formulas)
			# for formula_1 in formulas:
			# 	print formula_1.formula, "|"
			if isInAtom(formula.formula, formulas):
				return True
	return False


def isSatisfied(formula, tcc_structure, model_checking_atoms, model_checking_scc_subgraphs):
	initial_nodes = getInitialNodes(tcc_structure,model_checking_atoms)
	for scc_graph in model_checking_scc_subgraphs:
		selfFulfillingSCC = isSelfFulfilling(scc_graph, initial_nodes, model_checking_atoms)
		entailFormula = initialNodesEntailFormula(scc_graph, initial_nodes, model_checking_atoms,formula)
		print "SCC Graph: ", scc_graph
		print "is Self Fulfilling: ", selfFulfillingSCC
		print "Initial Nodes Entail Formula: ", entailFormula
		if selfFulfillingSCC and entailFormula:
			return True
	return False