# Filename: printGraphs.py

"""
This module contains the function that draws a graph in a .pdf file.
"""

__author__ = "Jaime E. Arias Almeida"
__license__ = "beerware"
__version__ = "1.0"
__email__ = "jearias@javerianacali.edu.co"
__docformat__ = 'reStructuredText'

import pydot

def drawGraph(graph, filename):
	"""
		Draws a graph and saves it to a .pdf file.
		
		:param graph: Graph.
		:type graph: Dictionary
		
		:param filename: Filename.
		:type filename: String
		
		:Example:
		
		>>> from printGraphs import *
		>>> graph = {3: [11, 13], 7: [11, 13], 11: [11, 13], 13: [27, 29], 17: [27, 29], 21: [27, 29], 27: [11, 13], 29: [27, 29]}
		>>> drawGraph(graph, 'scc_graph')
		
		.. figure:: ./scc_graph.png
			:align: center
			:height: 300px
			
			Graph drawn
		
		.. note::
			The generated PDF file is saved in the folder ``graph_files``.
					
	"""
	output_path = './graph_files/'
	
	colors = ["red", "blue", "orange", "violet", "red", "salmon2", "deepskyblue", "burlywood2", "greenyellow", "darkseagreen", "thistle2", "dodgerblue1", "darkolivegreen3", "chocolate", "turquoise3", "steelblue3", "navy", "coral", "blanchedalmond", "darkorange1", "goldenrod3", "firebrick", "chartreuse4", "crimson", "darkorange1", "darkolivegreen4"]

	dotGraph = pydot.Dot(graph_type='digraph', rankdir='LR')
	dotGraph.set_node_defaults(shape='circle')
	dotGraph.set_edge_defaults(arrowhead='vee')

	nodes = {}
	for node in graph.keys():
		nodes[node] = pydot.Node(str(node), color=colors[node%len(colors)], fontcolor=colors[node%len(colors)] )
		dotGraph.add_node(nodes[node])

	for node in graph.keys():
		next_nodes = graph.get(node)
		if len(next_nodes) != 0:
			for next_node in next_nodes:
				edge = pydot.Edge(nodes[node], nodes[next_node], color=colors[node%len(colors)])
				dotGraph.add_edge(edge)

	
	dotGraph.write_pdf(output_path+filename+".pdf")