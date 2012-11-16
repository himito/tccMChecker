# Filename: searchingAlgorithm.py

"""
This module contains the necessary functions to check if a model checking graph satisfies a property.
"""

__author__ = "Jaime E. Arias Almeida"
__license__ = "beerware"
__version__ = "1.0"
__email__ = "jearias@javerianacali.edu.co"
__docformat__ = 'reStructuredText'


import itertools
from formula import Formula
from modelCheckingGraph import searchFormulas, isInAtom


def getInitialNodes(tcc_structure,model_checking_atoms):
	"""
		Returns the initial nodes of a model checking graph.
		
		:param tcc_structure: tcc structure.
		:type tcc_structure: Dictionary
		
		:param model_checking_atoms: Model checking atoms.
		:type model_checking_atoms: Dictionary.
		
		:returns: A list with the number of the nodes that are initial nodes.
		:rtype: List of Integers
		
		:Example:
		
		>>> from searchingAlgorithm import *
		>>> getInitialNodes(tcc_structure,model_checking_atoms)
		[1, 2, 3, 4, 5, 6, 7, 8, 17, 18, 19, 20, 21, 22, 23, 24]
		
		.. seealso::
			:py:func:`modelCheckingGraph.getModelCheckingAtoms`
		
	"""
	initial_nodes = []
	for node in tcc_structure.keys():
		if tcc_structure.get(node).get("initial"):
			initial_nodes.append(model_checking_atoms.get(node).keys())
	return list(itertools.chain(*initial_nodes))
		

def getModelCheckingSCCSubgraphs(scc_list,tcc_structure,model_checking_atoms,model_checking_graph):
	"""
		Returns the Strongly Connected Component (SCC) subgraphs of a model checking graph.
		
		:param scc_list: List of the nodes corresponding to all of SCCs in the model checking graph.
		:type scc_list: List of Lists
		
		:param tcc_structure: tcc structure that represents the behavior of the system.
		:type tcc_structure: Dictionary
		
		:param model_checking_atoms: Model checking atoms.
		:type model_checking_atoms: List of atoms
		
		:param model_checking_graph: Model Checking graph
		:type model_checking_graph: Dictionary
		
		:returns: A list with the SCC subgraphs.
		:rtype: List 
		
		:Example:
		
		>>> from searchingAlgorithm import *
		>>> from tarjan import tarjan
		>>> strongly_connected_components = tarjan(model_checking_graph)
		>>> getModelCheckingSCCSubgraphs(strongly_connected_components, tcc_structure, model_checking_atoms,model_checking_graph)
		[{3: [11, 13], 7: [11, 13], 11: [11, 13], 13: [27, 29], 17: [27, 29], 21: [27, 29], 27: [11, 13], 29: [27, 29]}]
		
		.. figure:: ./example_scc.png
			:align: center
			:height: 200px
			
			SCC subgraph generated.
		
		.. note::
			To generate all the SCCs of a graph we use the `Tarjan's Algorithm <https://github.com/bwesterb/py-tarjan/>`_.
		
		.. seealso::
			:py:func:`modelCheckingGraph.getModelCheckingAtoms`, :py:func:`modelCheckingGraph.getModelCheckingGraph` 
		
	"""
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
	"""
		Returns the formulas of a specific model checking node.
		
		:param node: Number of the model checking node.
		:type node: Integer
		
		:param model_checking_atoms: Model checking atoms.
		:type model_checking_atoms: List of atoms.
		
		:returns: List of formulas of the node.
		:rtype: List of :py:class:`~formula.Formula`.
		
		:Example:
		
		>>> from searchingAlgorithm import *
		>>> formulas = getFormulas(3, model_checking_atoms)
		>>> for formula in basicFormulas:
		...     print formula.getFormula()
		{'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=1'}}}}}
		{'': 'in=true'}
		{'~': {'o': 'x=1'}}
		{'': 'x=1'}
		{'o': {'~': 'x=1'}}
		{'<>': {'^': {'': 'in=true', '~': {'o': 'x=1'}}}}
		{'^': {'': 'in=true', '~': {'o': 'x=1'}}}
		
		.. seealso::
			:py:func:`modelCheckingGraph.getModelCheckingAtoms`
		
	"""
	for tcc_node in model_checking_atoms.keys():
		if node in model_checking_atoms.get(tcc_node).keys():
			return model_checking_atoms[tcc_node].get(node)


def isSelfFulfilling(scc_graph, initial_nodes, model_checking_atoms):
	"""
		Checks if a SCC graph is a self-fulfilling SCC graph.
		
		:param scc_graph: SCC graph
		:type scc_graph: Dictionary
		
		:param initial_nodes: List of initial nodes of the model checking graph.
		:type initial_nodes: List
		
		:param model_checking_atoms: Model checking atoms
		:type model_checking_atoms: List of atoms.
		
		:returns: ``True`` if the graph is a self-fulfilling SCC or ``False`` otherwise.
		:rtype: Boolean
		
		:Example:
		
		>>> from searchingAlgorithm import *
		>>> sccGraph = {3: [11, 13], 7: [11, 13], 11: [11, 13], 13: [27, 29], 17: [27, 29], 21: [27, 29], 27: [11, 13], 29: [27, 29]}
		>>> initialNodes = [1, 2, 3, 4, 5, 6, 7, 8, 17, 18, 19, 20, 21, 22, 23, 24]
		>>> isSelfFulfilling(sccGraph, initialNodes, model_checking_atoms)
		True
		
		.. seealso::
			:py:func:`modelCheckingGraph.getModelCheckingAtoms`, :py:func:`.getModelCheckingSCCSubgraphs`, :py:func:`.getInitialNodes`
		
	"""
	# print "Checking if the graph is a self-fulfilling graph ..."
	for node in scc_graph.keys():
		if node not in initial_nodes:
			formulas = getFormulas(node,model_checking_atoms)
			diamond_formulas = searchFormulas(formulas, "<>")

			for diamond_formula in diamond_formulas:
				new_formula = Formula(diamond_formula.getValues())

				# print "search de node:", node,
				# print new_formula.getFormula()

				found = False
				for node_scc in scc_graph.keys():
					if node_scc not in initial_nodes:

						# print "en node: ", node_scc

						formulas_scc = getFormulas(node_scc, model_checking_atoms)
						# for formula in formulas_scc:
						# 	print formula.formula, "|"

						# print "Encontrado:", isInAtom(new_formula.getFormula(), formulas_scc)
						if isInAtom(new_formula.getFormula(), formulas_scc):
							found = True
							break
				if not found:
					return False
	return True


def initialNodesEntailFormula(scc_graph, initial_nodes, model_checking_atoms,formula):
	"""
		Checks if the initial nodes of a model checking graph satisfy a temporal formula.
		
		:param scc_graph: A SCC graph.
		:type scc_graph: Dictionary
		
		:param initial_nodes: Initial nodes of a model checking graph.
		:type initial_nodes: List of Integers
		
		:param model_checking_atoms: Model checking atoms
		:type model_checking_atoms: List of atoms
		
		:param formula: Formula 
		:type formula: :py:class:`~formula.Formula`.
		
		:returns: ``True`` if an initial node satisfies the formula or ``False`` otherwise.
		:rtype: Boolean.
		
		:Example: 
		
		>>> from formula import *
		>>> from searchingAlgorithm import *
		>>> formula = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=1"}}}})
		>>> sccGraph = {3: [11, 13], 7: [11, 13], 11: [11, 13], 13: [27, 29], 17: [27, 29], 21: [27, 29], 27: [11, 13], 29: [27, 29]}
		>>> initialNodes = [1, 2, 3, 4, 5, 6, 7, 8, 17, 18, 19, 20, 21, 22, 23, 24]
		>>> initialNodesEntailFormula(sccGraph, initialNodes, model_checking_atoms,formula)
		True
		
		.. seealso::
			:py:class:`formula.Formula`, :py:func:`modelCheckingGraph.getModelCheckingAtoms`, :py:func:`.getModelCheckingSCCSubgraphs`, :py:func:`.getInitialNodes`
		
	"""
	
	print "Formula:", formula.getFormula()
	for node in scc_graph.keys():
		if node in initial_nodes:
			formulas = getFormulas(node,model_checking_atoms)
			# print "node:", node
			# print "Entails:", isInAtom(formula.getFormula(), formulas)
			# for formula_1 in formulas:
			# 	print formula_1.formula, "|"
			if isInAtom(formula.getFormula(), formulas):
				return True
	return False
