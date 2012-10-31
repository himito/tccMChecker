
def parserGraphviz(graph):
	colors = ["red", "blue", "orange", "violet", "red", "salmon2", "deepskyblue", "burlywood2", "greenyellow", "darkseagreen", "thistle2", "dodgerblue1", "darkolivegreen3", "chocolate", "turquoise3", "steelblue3", "navy", "coral", "blanchedalmond", "darkorange1", "goldenrod3", "firebrick", "chartreuse4", "crimson", "darkorange1", "darkolivegreen4"]
	print "digraph G {"
	print "rankdir=LR"
	print 'size="8,5"'
	print "node [shape = circle];"
	print "edge [arrowhead = vee];"
	for node in graph.keys():
		print node, "[color = " + colors[node%len(colors)] + ", fontcolor = " + colors[node%len(colors)] +  "];"
	for node in graph.keys():
		next_nodes = graph.get(node)
		if len(next_nodes) != 0:
			for next_node in next_nodes:
				print node, "->", next_node,
				print "[color = " + colors[node%len(colors)] + "];"
	print "}"
