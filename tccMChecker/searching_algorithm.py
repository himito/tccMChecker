"""This module contains the necessary functions to check if a model checking
graph satisfies a property."""

from __future__ import print_function

import itertools

from model_checking_graph import search_formulas, is_in_atom

from tccMChecker.formula import Formula


def get_initial_nodes(tcc_structure, model_checking_atoms):
    """
    Returns the initial nodes of a model checking graph.

    :param tcc_structure: tcc structure.
    :type tcc_structure: Dictionary

    :param model_checking_atoms: Model checking atoms.
    :type model_checking_atoms: Dictionary.

    :returns: A list with the number of the nodes that are initial nodes.
    :rtype: List of Integers

    :Example:

    >>> from tccMChecker.searching_algorithm import *
    >>> get_initial_nodes(tcc_structure, model_checking_atoms)
    [1, 2, 3, 4, 5, 6, 7, 8, 17, 18, 19, 20, 21, 22, 23, 24]

    .. seealso::
        :py:func:`modelCheckingGraph.getModelCheckingAtoms`

    """
    initial_nodes = []
    for node in tcc_structure.keys():
        if tcc_structure.get(node).get("initial"):
            initial_nodes.append(model_checking_atoms.get(node).keys())
    return list(itertools.chain(*initial_nodes))


def get_model_checking_scc_subgraphs(scc_list, tcc_structure,
                                     model_checking_atoms,
                                     model_checking_graph):
    """
    Returns the Strongly Connected Component (SCC) subgraphs of a model
    checking graph.

    :param scc_list: List of the nodes corresponding to all of SCCs in the model
        checking graph.
    :type scc_list: List of Lists

    :param tcc_structure: tcc structure that represents the behavior of the
        system.
    :type tcc_structure: Dictionary

    :param model_checking_atoms: Model checking atoms.
    :type model_checking_atoms: List of atoms

    :param model_checking_graph: Model Checking graph
    :type model_checking_graph: Dictionary

    :returns: A list with the SCC subgraphs.
    :rtype: List

    :Example:

    >>> from tccMChecker.searching_algorithm import *
    >>> from tarjan import tarjan
    >>> strongly_connected_components = tarjan(model_checking_graph)
    >>> get_model_checking_scc_subgraphs(strongly_connected_components, tcc_structure, model_checking_atoms,model_checking_graph)
    [{3: [11, 13], 7: [11, 13], 11: [11, 13], 13: [27, 29], 17: [27, 29], 21: [27, 29], 27: [11, 13], 29: [27, 29]}]

    .. figure:: ./img/example_scc.png
        :align: center
        :height: 200px

        SCC subgraph generated.

    .. note::
        To generate all the SCCs of a graph we use the Tarjan's Algorithm.

    .. seealso::
        :py:func:`modelCheckingGraph.getModelCheckingAtoms`,
        :py:func:`modelCheckingGraph.getModelCheckingGraph`

    """
    initial_nodes = get_initial_nodes(tcc_structure, model_checking_atoms)
    model_checking_subgraphs = []

    for scc in scc_list:
        if len(scc) > 1:  # non-trivial
            temp_graph = {}
            for node in scc:
                nodes = list(set(model_checking_graph.get(node)).intersection(
                    set(scc)))
                if len(nodes) != 0:
                    temp_graph[node] = nodes

            for node in initial_nodes:
                nodes = list(set(model_checking_graph.get(node)).intersection(
                    set(scc)))
                if len(nodes) != 0:
                    temp_graph[node] = nodes

            model_checking_subgraphs.append(temp_graph)
    return model_checking_subgraphs


def get_formulas(node, model_checking_atoms):
    """
    Returns the formulas of a specific model checking node.

    :param node: Number of the model checking node.
    :type node: Integer

    :param model_checking_atoms: Model checking atoms.
    :type model_checking_atoms: List of atoms.

    :returns: List of formulas of the node.
    :rtype: List of :py:class:`~formula.Formula`.

    :Example:

    >>> from tccMChecker.searching_algorithm import *
    >>> formulas = get_formulas(3, model_checking_atoms)
    >>> for formula in formulas:
    ...     print(formula.get_formula())
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


def is_self_fulfilling(scc_graph, initial_nodes, model_checking_atoms):
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

    >>> from tccMChecker.searching_algorithm import *
    >>> sccGraph = {3: [11, 13], 7: [11, 13], 11: [11, 13], 13: [27, 29], 17: [27, 29], 21: [27, 29], 27: [11, 13], 29: [27, 29]}
    >>> initialNodes = [1, 2, 3, 4, 5, 6, 7, 8, 17, 18, 19, 20, 21, 22, 23, 24]
    >>> is_self_fulfilling(sccGraph, initialNodes, model_checking_atoms)
    True

    .. seealso::
        :py:func:`modelCheckingGraph.getModelCheckingAtoms`,
        :py:func:`.getModelCheckingSCCSubgraphs`, :py:func:`.getInitialNodes`

    """
    for node in scc_graph.keys():
        if node not in initial_nodes:
            formulas = get_formulas(node, model_checking_atoms)
            diamond_formulas = search_formulas(formulas, "<>")

            for diamond_formula in diamond_formulas:
                new_formula = Formula(diamond_formula.get_values())

                found = False
                for node_scc in scc_graph.keys():
                    if node_scc not in initial_nodes:

                        formulas_scc = get_formulas(node_scc,
                                                    model_checking_atoms)

                        if is_in_atom(new_formula.get_formula(), formulas_scc):
                            found = True
                            break
                if not found:
                    return False
    return True


def initial_nodes_entail_formula(scc_graph, initial_nodes, model_checking_atoms,
                                 formula):
    """
    Checks if the initial nodes of a model checking graph satisfy a temporal
    formula.

    :param scc_graph: A SCC graph.
    :type scc_graph: Dictionary

    :param initial_nodes: Initial nodes of a model checking graph.
    :type initial_nodes: List of Integers

    :param model_checking_atoms: Model checking atoms
    :type model_checking_atoms: List of atoms

    :param formula: Formula
    :type formula: :py:class:`~formula.Formula`.

    :returns: ``True`` if an initial node satisfies the formula or ``False``
        otherwise.
    :rtype: Boolean.

    :Example:

    >>> from tccMChecker.searching_algorithm import *
    >>> formula = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=1"}}}})
    >>> sccGraph = {3: [11, 13], 7: [11, 13], 11: [11, 13], 13: [27, 29], 17: [27, 29], 21: [27, 29], 27: [11, 13], 29: [27, 29]}
    >>> initialNodes = [1, 2, 3, 4, 5, 6, 7, 8, 17, 18, 19, 20, 21, 22, 23, 24]
    >>> initial_nodes_entail_formula(sccGraph, initialNodes, model_checking_atoms,formula)
    True

    .. seealso::
        :py:class:`formula.Formula`,
        :py:func:`modelCheckingGraph.getModelCheckingAtoms`,
        :py:func:`.getModelCheckingSCCSubgraphs`, :py:func:`.getInitialNodes`

    """

    print("Formula:", formula.get_formula())
    for node in scc_graph.keys():
        if node in initial_nodes:
            formulas = get_formulas(node, model_checking_atoms)
            if is_in_atom(formula.get_formula(), formulas):
                return True

    return False
