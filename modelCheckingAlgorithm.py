# Filename: modelCheckingAlgorithm.py

"""
This module contains the function that determines if a model satisfies a property.
"""

__author__ = "Jaime E. Arias Almeida"
__license__ = "beerware"
__version__ = "1.0"
__email__ = "jearias@javerianacali.edu.co"
__docformat__ = 'reStructuredText'

from formula import Formula
from closure import getClosure
from modelCheckingGraph import getAllAtoms, getModelCheckingAtoms, getModelCheckingGraph
from searchingAlgorithm import getModelCheckingSCCSubgraphs, getInitialNodes, isSelfFulfilling, initialNodesEntailFormula
from tarjan import tarjan
#from printGraphs import drawGraph


def modelSatisfiesProperty(formula, tcc_structure):
    """
        Checks if a model satisfies a formula.
        
        :param formula: Formula 
        :type formula: :py:class:`~formula.Formula`
        
        :param tcc_structure: tcc Structure
        :type tcc_structure: Dictionary
        
        :returns: ``True`` if the model satisfies the formula or ``False`` otherwise.
        :rtype: Boolean
        
        :Example:
        
        >>> from modelCheckingAlgorithm import *
        >>> tcc_structure = {
        ... 1: {"store": [Formula({"":"in=true"})], "normal": [], "temporal": ["t4","p9"], "edges": [2,3], "initial": True},
        ... 2: {"store": [Formula({"": "x=2"}),Formula({"": "in=true"})], "normal": [], "temporal": ["t4","p9"], "edges": [2,3], "initial": False},
        ... 3: {"store": [Formula({"": "x=2"}),Formula({"~": "in=true"})], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6], "initial": False},
        ... 4: {"store": [Formula({"~": "in=true"})], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6], "initial": True},
        ... 5: {"store": [Formula({"": "x=1"}),Formula({"": "in=true"})], "normal": [], "temporal": ["t4","p9"], "edges": [2,3], "initial": False},
        ... 6: {"store": [Formula({"": "x=1"}),Formula({"~": "in=true"})], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6], "initial": False}
        ... }
        >>> formula = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
        >>> modelSatisfiesProperty(formula, tcc_structure)
        False
        
        .. note::
            The model checking algorithm is based on the work performed by Falaschi and Villanueva [FV06]_. For this reason, we need to use the negation of the formula as input of this function and we say that the model satisfies the property if this function returns ``False`` (i.e the model does not satisfy the negation of the formula).
            
        .. seealso::
            :py:class:`formula.Formula`
        
    """
    
    # Closure
    closure = []
    getClosure(formula,closure)

    print "Clausura: ", len(closure)
    for formula_closure in closure:
        print formula_closure.getFormula()

    # All possible atoms
    atoms = getAllAtoms(closure)

#    print "============================================================================"
#    i=1
#    for atom in atoms:
#        print "Atomo: ",i
#        for f in atom:
#            print f.getFormula()
#        print "--------------------------------"
#        i=i+1


    # Model Checking Atoms
    model_checking_atoms = getModelCheckingAtoms(tcc_structure,atoms)

    for tcc_node in model_checking_atoms.keys():
        print "Atoms State", tcc_node, "(", len(model_checking_atoms.get(tcc_node)), ")"
        tcc_atoms = model_checking_atoms.get(tcc_node)
        for atom_index in tcc_atoms.keys():
            print "Atom ", atom_index
            for formula_atom in tcc_atoms.get(atom_index):
                print formula_atom.getFormula(), " | ",
            print "\n"  

    ## Model Checking Graph
    #model_checking_graph = getModelCheckingGraph(tcc_structure, model_checking_atoms)
    #print "Model Checking Graph"
    #print model_checking_graph
    
    ## Strongly Connected Components
    #strongly_connected_components = tarjan(model_checking_graph)
    #print "Strongly Connected Components : "
    #print strongly_connected_components
    
    #model_checking_scc_subgraphs = getModelCheckingSCCSubgraphs(strongly_connected_components, tcc_structure, model_checking_atoms,model_checking_graph)
    #print "Model Checking SCC Subgraphs (", len(model_checking_scc_subgraphs), ")"
    #print model_checking_scc_subgraphs
    
    ## Draw Graphs
    ##drawGraph(model_checking_graph, "modelCheckingGraph")
    ##for index, sccSubgraph in enumerate(model_checking_scc_subgraphs):
    ##   drawGraph(sccSubgraph, "SCC_Subgraph_"+str(index+1))
    
    ## Self-Fulfilling SCC and Initial Nodes
    #initial_nodes = getInitialNodes(tcc_structure,model_checking_atoms)
    #for scc_graph in model_checking_scc_subgraphs:
        #selfFulfillingSCC = isSelfFulfilling(scc_graph, initial_nodes, model_checking_atoms)
        #entailFormula = initialNodesEntailFormula(scc_graph, initial_nodes, model_checking_atoms,formula)
        #print "SCC Graph: ", scc_graph
        #print "is Self Fulfilling: ", selfFulfillingSCC
        #print "Initial Nodes Entail Formula: ", entailFormula
        #if selfFulfillingSCC and entailFormula:
            #return True
    #return False


# Main
if __name__ == "__main__":
    
    # TCC Structure
    tcc_structure = {   1: {"store": [Formula({"":"da=0"}),
                                      Formula({"^":{"": "b=1", " ":"sm=0"}}),
                                      Formula({"~":{"^":{"":"b=2", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=3", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=5"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=10"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=0"}}})
                                      ],
                            "normal": [],
                            "temporal": ["p27"],
                            "edges": [1,2,3,4,5,6],
                            "initial": True
                            },
                        2: {"store": [Formula({"":"da=0"}),
                                      Formula({"~":{"^":{"":"b=1", " ":"sm=0"}}}),
                                      Formula({"^":{"": "b=2", " ":"sm=0"}}),
                                      Formula({"~":{"^":{"":"b=3", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=5"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=10"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=0"}}})
                                      ],
                            "normal": [],
                            "temporal": ["p31"],
                            "edges": [1,2,3,4,5,6],
                            "initial": True
                            },
                        3: {"store": [Formula({"":"da=0"}),
                                      Formula({"~":{"^":{"":"b=1", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=2", " ":"sm=0"}}}),
                                      Formula({"^":{"": "b=3", " ":"sm=0"}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=5"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=10"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=0"}}})
                                      ],
                            "normal": [],
                            "temporal": ["p35"],
                            "edges": [1,2,3,4,5,6],
                            "initial": True
                            },
                        4: {"store": [Formula({"":"da=0"}),
                                      Formula({"~":{"^":{"":"b=1", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=2", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=3", " ":"sm=0"}}}),
                                      Formula({"^":{"": "b=0", " ":"sm=5"}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=10"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=0"}}})
                                      ],
                            "normal": [],
                            "temporal": ["p39"],
                            "edges": [7,8,9,10,11,12],
                            "initial": True
                            },
                        5: {"store": [Formula({"":"da=0"}),
                                      Formula({"~":{"^":{"":"b=1", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=2", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=3", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=5"}}}),
                                      Formula({"^":{"": "b=0", " ":"sm=10"}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=0"}}})
                                      ],
                            "normal": [],
                            "temporal": ["p43"],
                            "edges": [13,14,15,16,17,18],
                            "initial": True
                            },
                        6: {"store": [Formula({"":"da=0"}),
                                      Formula({"~":{"^":{"":"b=1", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=2", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=3", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=5"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=10"}}}),
                                      Formula({"^":{"": "b=0", " ":"sm=0"}}),
                                      ],
                            "normal": [],
                            "temporal": ["p46"],
                            "edges": [1,2,3,4,5,6],
                            "initial": True
                            },
                        7: {"store": [Formula({"":"da=5"}),
                                      Formula({"^":{"": "b=1", " ":"sm=0"}}),
                                      Formula({"~":{"^":{"":"b=2", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=3", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=5"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=10"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=0"}}})
                                      ],
                            "normal": [],
                            "temporal": ["p53"],
                            "edges": [7,8,9,10,11,12],
                            "initial": False
                            },
                        8: {"store": [Formula({"":"da=5"}),
                                      Formula({"~":{"^":{"":"b=1", " ":"sm=0"}}}),
                                      Formula({"^":{"": "b=2", " ":"sm=0"}}),
                                      Formula({"~":{"^":{"":"b=3", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=5"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=10"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=0"}}})
                                      ],
                            "normal": [],
                            "temporal": ["tell58","p59"],
                            "edges": [19],
                            "initial": False
                            },
                        9: {"store": [Formula({"":"da=5"}),
                                      Formula({"~":{"^":{"":"b=1", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=2", " ":"sm=0"}}}),
                                      Formula({"^":{"": "b=3", " ":"sm=0"}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=5"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=10"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=0"}}})
                                      ],
                            "normal": [],
                            "temporal": ["tell64","p65"],
                            "edges": [20],
                            "initial": False
                            },
                        10: {"store": [Formula({"":"da=5"}),
                                      Formula({"~":{"^":{"":"b=1", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=2", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=3", " ":"sm=0"}}}),
                                      Formula({"^":{"": "b=0", " ":"sm=5"}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=10"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=0"}}})
                                      ],
                            "normal": [],
                            "temporal": ["p69"],
                            "edges": [13,14,15,16,17,18],
                            "initial": False
                            },
                        11: {"store": [Formula({"":"da=5"}),
                                      Formula({"~":{"^":{"":"b=1", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=2", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=3", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=5"}}}),
                                      Formula({"^":{"": "b=0", " ":"sm=10"}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=0"}}})
                                      ],
                            "normal": [],
                            "temporal": ["tell74","p75"],
                            "edges": [21],
                            "initial": False
                            },
                        12: {"store": [Formula({"":"da=5"}),
                                      Formula({"~":{"^":{"":"b=1", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=2", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=3", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=5"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=10"}}}),
                                      Formula({"^":{"": "b=0", " ":"sm=0"}})
                                      ],
                            "normal": [],
                            "temporal": ["p78"],
                            "edges": [7,8,9,10,11,12],
                            "initial": False
                            },
                        13: {"store": [Formula({"":"da=10"}),
                                      Formula({"^":{"": "b=1", " ":"sm=0"}}),
                                      Formula({"~":{"^":{"":"b=2", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=3", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=5"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=10"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=0"}}})
                                      ],
                            "normal": [],
                            "temporal": ["tell86","p87"],
                            "edges": [22],
                            "initial": False
                            },
                        14: {"store": [Formula({"":"da=10"}),
                                      Formula({"~":{"^":{"":"b=1", " ":"sm=0"}}}),
                                      Formula({"^":{"": "b=2", " ":"sm=0"}}),
                                      Formula({"~":{"^":{"":"b=3", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=5"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=10"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=0"}}})
                                      ],
                            "normal": [],
                            "temporal": ["tell92","p93"],
                            "edges": [23],
                            "initial": False
                            },
                        15: {"store": [Formula({"":"da=10"}),
                                      Formula({"~":{"^":{"":"b=1", " ":"sm=0"}}}),
                                      Formula({"~":{"^":{"":"b=2", " ":"sm=0"}}}),
                                      Formula({"^":{"": "b=3", " ":"sm=0"}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=5"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=10"}}}),
                                      Formula({"~":{"^":{"":"b=0", " ":"sm=0"}}})
                                      ],
                            "normal": [],
                            "temporal": ["tell98","p99"],
                            "edges": [24],
                            "initial": False
                            },
                        16: {"store": [Formula({"":"da=10"}),
                                       Formula({"~":{"^":{"":"b=1", " ":"sm=0"}}}),
                                       Formula({"~":{"^":{"":"b=2", " ":"sm=0"}}}),
                                       Formula({"~":{"^":{"":"b=3", " ":"sm=0"}}}),
                                       Formula({"^":{"": "b=0", " ":"sm=5"}}),
                                       Formula({"~":{"^":{"":"b=0", " ":"sm=10"}}}),
                                       Formula({"~":{"^":{"":"b=0", " ":"sm=0"}}})
                                       ],
                            "normal": [],
                            "temporal": ["tell104","p105"],
                            "edges": [21],
                            "initial": False
                            },
                        17: {"store": [Formula({"":"da=10"}),
                                       Formula({"~":{"^":{"":"b=1", " ":"sm=0"}}}),
                                       Formula({"~":{"^":{"":"b=2", " ":"sm=0"}}}),
                                       Formula({"~":{"^":{"":"b=3", " ":"sm=0"}}}),
                                       Formula({"~":{"^":{"":"b=0", " ":"sm=5"}}}),
                                       Formula({"^":{"": "b=0", " ":"sm=10"}}),
                                       Formula({"~":{"^":{"":"b=0", " ":"sm=0"}}})
                                       ],
                            "normal": [],
                            "temporal": ["tell110","p111"],
                            "edges": [25],
                            "initial": False
                            },
                        18: {"store": [Formula({"":"da=10"}),
                                       Formula({"~":{"^":{"":"b=1", " ":"sm=0"}}}),
                                       Formula({"~":{"^":{"":"b=2", " ":"sm=0"}}}),
                                       Formula({"~":{"^":{"":"b=3", " ":"sm=0"}}}),
                                       Formula({"~":{"^":{"":"b=0", " ":"sm=5"}}}),
                                       Formula({"~":{"^":{"":"b=0", " ":"sm=10"}}}),
                                       Formula({"^":{"": "b=0", " ":"sm=0"}})
                                       ],
                            "normal": [],
                            "temporal": ["p114"],
                            "edges": [13,14,15,16,17,18],
                            "initial": False
                            },
                        19: {"store": [Formula({"":"da=0"}),
                                       Formula({"":"tt"}),
                                       Formula({"":"dc"})
                                       ],
                            "normal": [],
                            "temporal": ["p8"],
                            "edges": [1,2,3,4,5,6],
                            "initial": False
                            },
                        20: {"store": [Formula({"":"da=5"}),
                                       Formula({"":"dd"})
                                       ],
                            "normal": [],
                            "temporal": ["p13"],
                            "edges": [1,2,3,4,5,6],
                            "initial": False
                            },
                        21: {"store": [Formula({"":"da=15"}),
                                       Formula({"":"dd"})
                                       ],
                            "normal": [],
                            "temporal": ["p13"],
                            "edges": [1,2,3,4,5,6],
                            "initial": False
                            },
                        22: {"store": [Formula({"":"da=0"}),
                                       Formula({"":"tc"}),
                                       Formula({"":"dc"})
                                       ],
                            "normal": [],
                            "temporal": ["p20"],
                            "edges": [1,2,3,4,5,6],
                            "initial": False
                            },
                        23: {"store": [Formula({"":"da=5"}),
                                       Formula({"":"tt"}),
                                       Formula({"":"dc"})
                                       ],
                            "normal": [],
                            "temporal": ["p8"],
                            "edges": [1,2,3,4,5,6],
                            "initial": False
                            },
                        24: {"store": [Formula({"":"da=10"}),
                                       Formula({"":"dd"})
                                       ],
                            "normal": [],
                            "temporal": ["p13"],
                            "edges": [1,2,3,4,5,6],
                            "initial": False
                            },
                        25: {"store": [Formula({"":"da=20"}),
                                       Formula({"":"dd"})
                                       ],
                            "normal": [],
                            "temporal": ["p13"],
                            "edges": [1,2,3,4,5,6],
                            "initial": False
                            }
    }

    # Formula
    phi = Formula({"<>":{"^":{"^":{"":"da=5", " ":"b=1"}, "~":{"o":"tc"}}}})
    print "Formula: "
    print phi.getFormula()

    # Report
    print "***************** REPORT *****************"
    result = modelSatisfiesProperty(phi, tcc_structure)
    print "Model Satisfies Formula: ", not result

















