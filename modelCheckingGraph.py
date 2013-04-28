# Filename: modelCheckingGraph.py

"""
This module contains the necessary functions to generate a model checking graph.
"""

__author__ = "Jaime E. Arias Almeida"
__license__ = "beerware"
__version__ = "1.0"
__email__ = "jearias@javerianacali.edu.co"
__docformat__ = 'reStructuredText'

from formula import Formula

######################################## Atoms ########################################
def getBasicFormulas(closure):
    """
        Returns the basic formulas (i.e. propositions or formulas with :math:`\circ` as main connective) of the closure.

        :param closure: Closure of a formula.
        :type closure: List of :py:class:`~formula.Formula`

        :returns: List of basic formulas of the closure.
        :rtype: List of :py:class:`~formula.Formula`.

        :Example:

        >>> from closure import *
        >>> from modelCheckingGraph import *
        >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
        >>> closure = []
        >>> getClosure(phi,closure)
        >>> basicFormulas = getBasicFormulas(closure)
        >>> for formula in basicFormulas:
        ...     print formula.getFormula()
        ... 
        {'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}
        {'': 'in=true'}
        {'o': 'x=2'}
        {'': 'x=2'}

        .. seealso::
            :py:func:`closure.getClosure`, :py:class:`formula.Formula`

    """
    basicFormulas = []
    for formula in closure:
        if formula.isBasic():
            basicFormulas.append(formula)
    return basicFormulas

def getNoBasicFormulas(closure):
    """
        Returns the formulas of the closure that are not basic formulas.
        
        :param closure: Closure of a formula.
        :type closure: List of :py:class:`~formula.Formula`
        
        :returns: List of formulas of the closure that are not basic formulas.
        :rtype: List of :py:class:`~formula.Formula`.
        
        :Example:
        
        >>> from closure import *
        >>> from modelCheckingGraph import *
        >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
        >>> closure = []
        >>> getClosure(phi,closure)
        >>> noBasicFormulas = getNoBasicFormulas(closure)
        >>> for formula in noBasicFormulas:
        ...     print formula.getFormula()
        ... 
        {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
        {'^': {'': 'in=true', '~': {'o': 'x=2'}}}
        
        .. seealso::
            :py:func:`closure.getClosure`, :py:class:`formula.Formula`
        
    """
    result = []
    for formula in closure:
        if formula.getConnective() != "~" and formula.getConnective() != "o" and not formula.isProposition():
            result.append(formula)
    return result
    

def searchFormulas(formulas, connective):
    """
        Returns the formulas that have a particular main connective.
        
        :param formulas: List of formulas.
        :type formulas: List of :py:class:`~formula.Formula`
        
        :param connective: The main connective.
        :type connective: String
        
        :returns: List containing the formulas that have the main connective.
        :rtype: List
        
        :Example:
        
        >>> from modelCheckingGraph import *
        >>> list = [Formula({'o': 'x=2'}), Formula({'~': {'o': 'x=2'}}), Formula({'o': {'~': 'x=2'}})]
        >>> result = searchFormulas(list,'o')
        >>> for formula in result:
        ...     print formula.getFormula()
        ... 
        {'o': 'x=2'}
        {'o': {'~': 'x=2'}}
        
    """
    result = []
    for formula in formulas:
        if formula.getConnective() == connective:
            result.append(formula)
    return result

def getAllAtoms(closure):
    """
        Returns all possible atoms of the closure.
        
        :param closure: Closure of a formula.
        :type closure: List of :py:class:`~formula.Formula`
        
        :returns: List of all atoms of the closure.
        :rtype: List of lists of :py:class:`~formula.Formula`.
        
        :Example:
        
        >>> from closure import *
        >>> from modelCheckingGraph import *
        >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
        >>> closure = []
        >>> getClosure(phi,closure)
        >>> atoms = getAllAtoms(closure)
        >>> for index, atom in enumerate(atoms):
        ...     print "Atom " + str(index) + ":"
        ...     for formula in atom:
        ...             print formula.getFormula()
        ... 
        Atom 0:
        {'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}
        {'': 'in=true'}
        {'o': 'x=2'}
        {'': 'x=2'}
        {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
        {'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
        Atom 1:
        {'~': {'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}}
        {'': 'in=true'}
        {'o': 'x=2'}
        {'': 'x=2'}
        {'o': {'~': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}}
        {'~': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}
        {'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
        ...
        
        .. seealso::
            :py:func:`closure.getClosure`, :py:class:`formula.Formula`
        
        .. note::
        
            This function is based on the algorithm shown in [MP95]_.
        
    """
    basicFormulas = getBasicFormulas(closure)
    noBasicFormulas = getNoBasicFormulas(closure)
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
    
    for formula in noBasicFormulas:
        for atom in atoms:
            if isConsistent(formula, atom):
                atom.append(formula)
            else: 
                atom.append(formula.getNegation())

    return atoms

def isInAtom(formula, atom):
    """
        Checks if a formula is in an atom.
        
        :param formula: Structure representing a formula.
        :type formula: Dictionary
        
        :param atom: List of consistent formulas representing an atom of the closure.
        :type atom: List of :py:class:`~formula.Formula`.
        
        :returns: ``True`` if the formula is in atom or ``False`` otherwise.
        :rtype: Boolean
        
        :Example:
        
        >>> from closure import *
        >>> from modelCheckingGraph import *
        >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
        >>> closure = []
        >>> getClosure(phi,closure)
        >>> atoms = getAllAtoms(closure)
        >>> isInAtom({'': 'in=true'}, atoms[0])
        True
        
        .. seealso::
            :py:func:`closure.getClosure`, :py:class:`formula.Formula`, :py:func:`.getAllAtoms`
    """
    for formulaAtom in atom:
        if formulaAtom.getFormula() == formula:
            return True
    return False


def cleanConector(formula):
    formula_temp = formula.getFormula()
    key = formula_temp.keys()[0]
    key_new = key.replace(" ","")
    formula_temp[key_new] = formula_temp.pop(key)
    return Formula(formula_temp)

    

def isConsistent(formula, atom):
    """
        Checks if a formula is consistent with the set of formulas in an atom.
        
        :param formula: Formula 
        :type formula: :py:class:`~formula.Formula`
        
        :param atom: List of consistent formulas representing an atom of the closure.
        :type atom: List of :py:class:`~formula.Formula`.
        
        :returns: ``True`` if the formula is consistent with the set of formulas in the atom or ``False`` otherwise.
        :rtype: Boolean
        
        :Example:
        
        >>> from closure import *
        >>> from modelCheckingGraph import *
        >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
        >>> closure = []
        >>> getClosure(phi,closure)
        >>> atoms = getAllAtoms(closure)
        >>> isConsistent(Formula({'': 'x=1'}), atoms[0])
        False
        
        .. seealso::
            :py:func:`closure.getClosure`, :py:class:`formula.Formula`, :py:func:`.getAllAtoms`
        
        .. note::
        
            This function is based on the conditions shown in the defintion 6.1 of the thesis document.
    """
#    rules = {"x=2": Formula({"~": "x=1"}), "x=1": Formula({"~": "x=2"})} # Change!
    formula = cleanConector(formula)
#    formula_temp = formula.getFormula()
#    key = formula_temp.keys()[0]
#    key_new = key.replace(" ","")
#    formula_temp[key_new] = formula_temp.pop(key)
#    formula = Formula(formula_temp)
    
    print "verificando: ", formula.getFormula()
    
    
    if not isInAtom(formula.getNegation().getFormula(), atom):
        if formula.getConnective() == "<>": # <> rules
            if isInAtom({"o": formula.getFormula()},atom) or isConsistent(Formula(formula.getValues()), atom):
                return True
        elif formula.getConnective() == "[]": # [] rules
            if isInAtom({"o": formula.getFormula()},atom) and isConsistent(Formula(formula.getValues()), atom):
                return True
        elif formula.getConnective() == "^": # ^ rules
            subformulas = formula.getSubFormulas()
            if isConsistent(subformulas[0], atom) and isConsistent(subformulas[1], atom):
                return True
        elif formula.getConnective() == "v": # v rules
            subformulas = formula.getSubFormulas()
            if isConsistent(subformulas[0], atom) or isConsistent(subformulas[1], atom):
                return True
        elif formula.isProposition() or formula.getConnective() == "o" or formula.isNegativeNext():
            if (formula.isProposition() and formula.getConnective() == ""):
                if propositionConsistent(formula, atom):
                    return True
            elif (formula.isProposition() and formula.getConnective() == "~"):
                print "No esta la negacion"
                return True
            elif(formula.getFormula().keys()[0]== " "): # cuando es {" ": values}
                if isInAtom({"": formula.getFormula().values()[0]}, atom):
                    return True
            elif isInAtom(formula.getFormula(), atom):
                return True
            
    return False



######################################## Atoms  for tcc nodes ########################################

def deleteAtoms(atoms, index_list):
    """
        Removes atoms from a list of atoms.
        
        :param atoms: List of atoms.
        :type atoms: List of lists
        
        :param index_list: Index list of the elements to be removed. 
        :type index_list: List
        
        :returns: List of atoms with atoms removed.
        :rtype: List.
        
        :Example:
        
        >>> from closure import *
        >>> from modelCheckingGraph import *
        >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
        >>> closure = []
        >>> getClosure(phi,closure)
        >>> atoms = getAllAtoms(closure)
        >>> len(atoms)
        16
        >>> newAtoms = deleteAtoms(atoms,[0,2,3,4,5,6,7,8,9,10,11,12,14,15])
        >>> len(newAtoms)
        2
        
        .. seealso::
            :py:func:`closure.getClosure`, :py:class:`formula.Formula`, :py:func:`.getAllAtoms`
    """
    result = []
    index = 0
    while index < len(atoms):
        if index in index_list:
            result.insert(0,atoms[index])
        else:
            result.append(atoms[index])
        index +=1
    return result[len(index_list):]

def propositionConsistent(formula, atom):
    """
        Checks if a proposition is consistent with the formulas of an atom.
        
        :param formula: Formula
        :type formula: :py:class:`~formula.Formula`
        
        :param atom: Atom
        :type atom: List of :py:class:`~formula.Formula`
        
        :returns: ``True`` if the proposition is consistent with the atom or ``False`` otherwise.
        :rtype: Boolean.
        
        :Example:
        
        >>> from closure import *
        >>> from modelCheckingGraph import *
        >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
        >>> closure = []
        >>> getClosure(phi,closure)
        >>> atoms = getAllAtoms(closure)
        >>> proposition = Formula({"~":"x=2"})
        >>> atom = atoms[0]
        >>> for formula in atom:
        ...     print formula.getFormula()
        ... 
        {'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}
        {'': 'in=true'}
        {'o': 'x=2'}
        {'': 'x=2'}
        {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
        {'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
        >>> propositionConsistent(proposition, atom)
        False
        
        .. seealso::
            :py:func:`closure.getClosure`, :py:class:`formula.Formula`, :py:func:`.getAllAtoms`
        
    """
    print "ES PROPOSICION"
    if formula.isProposition() and (formula.getValues() in formula.getPropositionRules().keys()):
        no_consistent_propositions= formula.getConsistentPropositions()
        for no_consistent_proposition in no_consistent_propositions:
            print "esta", no_consistent_proposition, " en el atomo: ",
            if isInAtom(no_consistent_proposition, atom):
                print "Si, por lo tanto NO ES CONSISTENTE"
                return False
            print "no"
        print "No hay ninguna incosistencia, por lo tanto es CONSISTENTE"
        return True
    return False
    
def list2dict(lists, offset):
    """
        Converts a list to a dictionary with ascending numbers as keys.
        
        :param lists: List with elements.
        :type lists: List
        
        :param offset: Offset of numeration.
        :type offset: Integer
        
        :returns: Dictionary with numbers as keys, and elements of the list as values. 
        :rtype: Dictionary.
        
        :Example:
        
        >>> from modelCheckingGraph import *
        >>> list = ["I", "Love", "Computer", "Science"]
        >>> list2dict(list, 2)
        {2: 'I', 3: 'Love', 4: 'Computer', 5: 'Science'}
         
    """
    result = {}
    for index, element in enumerate(lists):
        result[index+offset] = element
    return result

def getTotalNodes(graph):
    """
        Returns the total number of atoms.
        
        :param graph: Dictionary representing the atoms in each tcc state.
        :type graph: Dictionary
        
        :returns: The total number of atoms.
        :rtype: Integer
        
        :Example:
        
        >>> from modelCheckingGraph import *
        >>>> graph = {1: [[Formula({'': 'in=true'}), Formula({'o': 'x=2'})],
        ... [Formula({'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}})]],
        ... 2: [[Formula({'~': 'in=true'}),Formula({'~': {'o': 'x=2'}})]]}
        >>> getTotalNodes(graph)
        3
        
        .. seealso::
            :py:class:`formula.Formula`     
        
    """
    total = 0
    for index_node in graph.keys():
        total = total + len(graph.get(index_node))
    return total
    
def getModelCheckingAtoms(tcc_structure, atoms):
    """
        Returns the atoms corresponding to the states of a tcc structure.
        
        :param tcc_structure: Structure representing the behaviour of a system.
        :type tcc_structure: Dictionary
        
        :param atoms: List of all possible atoms of closure.
        :type atoms: List of atoms
        
        :returns: Dictionary that have the states of a tcc structure as keys, and a list of consistent atoms as values.
        :rtype: Dictionary
        
        :Example:

        >>> from modelCheckingGraph import *
        >>> from closure import *
        >>> tcc_structure = { 
        ... 1: {"store": [Formula({"":"in=true"})], "normal": [], "temporal": ["t4","p9"], "edges": [2,3], "initial": True},
        ... 2: {"store": [Formula({"": "x=2"}),Formula({"": "in=true"})], "normal": [], "temporal": ["t4","p9"], "edges": [2,3], "initial": False},
        ... 3: {"store": [Formula({"": "x=2"}),Formula({"~": "in=true"})], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6], "initial": False},
        ... 4: {"store": [Formula({"~": "in=true"})], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6], "initial": True},
        ... 5: {"store": [Formula({"": "x=1"}),Formula({"": "in=true"})], "normal": [], "temporal": ["t4","p9"], "edges": [2,3], "initial": False},
        ... 6: {"store": [Formula({"": "x=1"}),Formula({"~": "in=true"})], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6], "initial": False}
        ... }
        >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
        >>> closure = []
        >>> getClosure(phi,closure)
        >>> atoms = getAllAtoms(closure)
        >>> model_checking_atoms = getModelCheckingAtoms(tcc_structure,atoms)
        >>> for tcc_node in model_checking_atoms.keys():
        ...     print "tcc State", tcc_node
        ...     tcc_atoms = model_checking_atoms.get(tcc_node)
        ...     for atom_index in tcc_atoms.keys():
        ...             print "Atom ", atom_index
        ...             for formula in tcc_atoms.get(atom_index):
        ...                     print formula.getFormula(), " | ",
        ...             print "\\n"
        tcc State 1
        Atom  1
        {'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}  |  {'': 'in=true'}  |  {'o': 'x=2'}  |  {'': 'x=2'}  |  {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}  |  {'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}  |         
        Atom  2
        {'~': {'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}}  |  {'': 'in=true'}  |  {'o': 'x=2'}  |  {'': 'x=2'}  |  {'o': {'~': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}}  |  {'~': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}  |  {'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}  |

        .. seealso::
            :py:func:`closure.getClosure`, :py:class:`formula.Formula`, :py:func:`.getAllAtoms` 
    """
    model_checking_atoms = {}
    for tcc_node in tcc_structure.keys():
        atoms_node = atoms
        propositions = tcc_structure.get(tcc_node).get("store")
        for proposition in propositions: # Propositions as formulas
            index_atom = 0
            delete_atoms = []
            while index_atom < len(atoms_node):
                atom = atoms_node[index_atom]
                
                print "----------------------------------------------------------------------"
                print "evaluating proposition: ", proposition.getFormula()
                for f in atom:
                    print f.getFormula()
        
                if  isConsistent(proposition,atom):
                    print "ES CONSISTENTE"
                    if (proposition.getConnective() == "^"):
                        subformulas = proposition.getSubFormulas()
                        if not isInAtom(subformulas[0].getFormula(),atom):
                            atoms_node[index_atom].append(cleanConector(subformulas[0]))
                        if not isInAtom(subformulas[1].getFormula(),atom):
                            atoms_node[index_atom].append(cleanConector(subformulas[1]))
            
                    if not isInAtom(proposition.getFormula(),atom):
                        atoms_node[index_atom].append(proposition)
                else:
                    print "NO ES CONSISTENTE"
                    delete_atoms.append(index_atom)
                index_atom +=1
            atoms_node = deleteAtoms(atoms_node,delete_atoms)
        model_checking_atoms[tcc_node] = list2dict(atoms_node,getTotalNodes(model_checking_atoms) + 1)
    return model_checking_atoms
    
######################################## Model Checking Graph ########################################

def isNextState(nextFormulas,nextAtom):
    """
        Checks if an atom satisfies a list of formulas with next operator as main connective. 

        :param nextFormulas: List of formulas with next operator as main connective.
        :type nextFormulas: List of :py:class:`~formula.Formula`

        :param nextAtom: Atom.
        :type nextAtom: List of :py:class:`~formula.Formula`

        :returns: ``True`` if the atom satisfies the termporal formulas or ``False`` otherwise.
        :rtype: Boolean

        :Example:

        >>> from modelCheckingGraph import *
        >>> atom = [Formula({'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}),
        ... Formula({'': 'in=true'}), Formula({'o': 'x=2'}), Formula({'': 'x=2'}),
        ... Formula({'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}),
        ... Formula({'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}})]
        >>> 
        >>> formulas = [Formula({'o': 'x=2'})]
        >>> isNextState(formulas,atom)
        True

        .. note::
            We say that an atom satisfies a list of formulas when for all the formulas :math:`\circ\phi` in the list we found a formula :math:`\phi` in the atom.

        .. seealso::
            :py:class:`formula.Formula`

    """
    for formula in nextFormulas:
        next = Formula(formula.getValues())
        if not isInAtom(next.getFormula(), nextAtom): 
            return False
    return True

def getModelCheckingGraph(tcc_structure, model_checking_atoms):
    """
        Returns the model checking graph
        
        :param tcc_structure: Estructure representing the behavior of a system.
        :type tcc_structure: Dictionary
        
        :param model_checking_atoms: Atoms of a tcc structure.
        :type model_checking_atoms: Dictionary
        
        :returns: Structure representing the model checking graph.
        :rtype: Dictionary
        
        :Example:
        
        >>> from modelCheckingGraph import *
        >>> from closure import *
        >>> tcc_structure = {
        ...  1: {"store": [Formula({"":"in=true"})], "normal": [], "temporal": ["t4","p9"], "edges": [2,3], "initial": True},
        ... 2: {"store": [Formula({"": "x=2"}),Formula({"": "in=true"})], "normal": [], "temporal": ["t4","p9"], "edges": [2,3], "initial": False},
        ... 3: {"store": [Formula({"": "x=2"}),Formula({"~": "in=true"})], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6], "initial": False},
        ... 4: {"store": [Formula({"~": "in=true"})], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6], "initial": True},
        ... 5: {"store": [Formula({"": "x=1"}),Formula({"": "in=true"})], "normal": [], "temporal": ["t4","p9"], "edges": [2,3], "initial": False},
        ... 6: {"store": [Formula({"": "x=1"}),Formula({"~": "in=true"})], "normal": ["now2"], "temporal": ["t7","p9"], "edges": [5,6], "initial": False}
        ... }
        >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
        >>> closure = []
        >>> getClosure(phi,closure)
        >>> atoms = getAllAtoms(closure)
        >>> model_checking_atoms = getModelCheckingAtoms(tcc_structure,atoms)
        >>> getModelCheckingGraph(tcc_structure, model_checking_atoms)
        {1: [9, 11, 12, 13, 15], 2: [10, 16, 14], 3: [], 4: [], 5: [9, 11, 12, 13, 15], 6: [10, 16, 14], 7: [], 8: [], 9: [9, 11, 12, 13, 15], 10: [10, 16, 14], 11: [], 12: [], 13: [], 14: [], 15: [25, 27, 28, 29, 31], 16: [26, 32, 30], 17: [], 18: [], 19: [25, 27, 28, 29, 31], 20: [26, 32, 30], 21: [], 22: [], 23: [25, 27, 28, 29, 31], 24: [26, 32, 30], 25: [9, 11, 12, 13, 15], 26: [10, 16, 14], 27: [], 28: [], 29: [], 30: [], 31: [25, 27, 28, 29, 31], 32: [26, 32, 30]}
        
        .. figure:: ./example_model_checking_graph.png
            :align: center
            :height: 400px
            
            Model checking graph generated.
        
        .. seealso::
            :py:func:`closure.getClosure`, :py:class:`formula.Formula`, :py:func:`.getAllAtoms`
    """
    model_checking_graph={}
    for tcc_node in tcc_structure.keys():
        atoms_tcc_node = model_checking_atoms.get(tcc_node)
        for index_n1 in atoms_tcc_node.keys():
            atom_n1  = atoms_tcc_node.get(index_n1)
            nextFormulas = searchFormulas(atom_n1,"o")
            next_nodes = []
            for next_tcc_node in tcc_structure[tcc_node].get("edges"):
                atoms_next_tcc_node = model_checking_atoms.get(next_tcc_node)
                for index_n2 in atoms_next_tcc_node.keys():
                    atom_n2 = atoms_next_tcc_node.get(index_n2)
                    if isNextState(nextFormulas, atom_n2):
                        # print "tcc state: ", tcc_node, "(", index_n1, ") -> ", "next tcc state", next_tcc_node, "(", index_n2, ")"
                        next_nodes.append(index_n2)
            model_checking_graph[index_n1] = next_nodes
    return model_checking_graph









