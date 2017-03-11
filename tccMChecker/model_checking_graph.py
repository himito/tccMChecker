"""This module contains the necessary functions to generate a model checking
graph."""

from __future__ import print_function

import copy

from formula import Formula


def get_basic_formulas(closure):
    r"""
    Returns the basic formulas (i.e. propositions or formulas with
    :math:`\circ` as main connective) of the closure.

    :param closure: Closure of a formula.
    :type closure: List of :py:class:`~formula.Formula`

    :returns: List of basic formulas of the closure.
    :rtype: List of :py:class:`~formula.Formula`.

    :Example:

    >>> from tccMChecker.closure import *
    >>> from tccMChecker.model_checking_graph import *
    >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
    >>> closure = []
    >>> get_closure(phi,closure)
    >>> basic_formulas = get_basic_formulas(closure)
    >>> for formula in basic_formulas:
    ...     print(formula.get_formula())
    ...
    {'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}
    {'': 'in=true'}
    {'o': 'x=2'}
    {'': 'x=2'}

    .. seealso::
        :py:func:`closure.getClosure`, :py:class:`formula.Formula`

    """
    basic_formulas = []
    for formula in closure:
        if formula.is_basic():
            basic_formulas.append(formula)
    return basic_formulas


def get_no_basic_formulas(closure):
    """
    Returns the formulas of the closure that are not basic formulas.

    :param closure: Closure of a formula.
    :type closure: List of :py:class:`~formula.Formula`

    :returns: List of formulas of the closure that are not basic formulas.
    :rtype: List of :py:class:`~formula.Formula`.

    :Example:

    >>> from tccMChecker.closure import *
    >>> from tccMChecker.model_checking_graph import *
    >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
    >>> closure = []
    >>> get_closure(phi,closure)
    >>> noBasicFormulas = get_no_basic_formulas(closure)
    >>> for formula in noBasicFormulas:
    ...     print(formula.get_formula())
    ...
    {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
    {'^': {'': 'in=true', '~': {'o': 'x=2'}}}

    .. seealso::
        :py:func:`closure.getClosure`, :py:class:`formula.Formula`
        
    """
    result = []
    for formula in closure:
        if formula.get_connective() != "~" and formula.get_connective() != "o" \
                and not formula.is_proposition():
            result.append(formula)
    return result


def search_formulas(formulas, connective):
    """
    Returns the formulas that have a particular main connective.

    :param formulas: List of formulas.
    :type formulas: List of :py:class:`~formula.Formula`

    :param connective: The main connective.
    :type connective: String

    :returns: List containing the formulas that have the main connective.
    :rtype: List

    :Example:

    >>> from tccMChecker.model_checking_graph import *
    >>> list = [Formula({'o': 'x=2'}), Formula({'~': {'o': 'x=2'}}), Formula({'o': {'~': 'x=2'}})]
    >>> result = search_formulas(list,'o')
    >>> for formula in result:
    ...     print(formula.get_formula())
    ...
    {'o': 'x=2'}
    {'o': {'~': 'x=2'}}
        
    """
    result = []
    for formula in formulas:
        if formula.get_connective() == connective:
            result.append(formula)
    return result


def get_all_atoms(closure):
    """
    Returns all possible atoms of the closure.

    :param closure: Closure of a formula.
    :type closure: List of :py:class:`~formula.Formula`

    :returns: List of all atoms of the closure.
    :rtype: List of lists of :py:class:`~formula.Formula`.

    :Example:

    >>> from tccMChecker.closure import *
    >>> from tccMChecker.model_checking_graph import *
    >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
    >>> closure = []
    >>> get_closure(phi,closure)
    >>> atoms = get_all_atoms(closure)
    >>> for index, atom in enumerate(atoms):
    ...     print("Atom " + str(index) + ":")
    ...     for formula in atom:
    ...             print(formula.get_formula())
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
    basic_formulas = get_basic_formulas(closure)
    no_basic_formulas = get_no_basic_formulas(closure)
    num_atoms = 2 ** len(basic_formulas)
    atoms = [[] for i in range(num_atoms)]

    # 2^b Combinations
    for index_basic_formula in range(len(basic_formulas)):
        num = 2 ** index_basic_formula
        index_negative = 0
        negative = False
        for index in range(num_atoms):
            if index_negative == num:
                negative = not negative
                index_negative = 0
            if negative:
                atoms[index].append(
                    basic_formulas[index_basic_formula].get_negation())
            else:
                atoms[index].append(basic_formulas[index_basic_formula])
            index_negative += 1

    # o~phi
    f_temps = search_formulas(basic_formulas, "o")
    for formula in f_temps:
        for atom in atoms:
            if formula not in atom:
                atom.append(Formula({"o": {"~": formula.get_values()}}))

    for formula in no_basic_formulas:
        for atom in atoms:
            if is_consistent(formula, atom):
                atom.append(formula)
            else:
                atom.append(formula.get_negation())

    return atoms


def is_in_atom(formula, atom):
    """
    Checks if a formula is in an atom.

    :param formula: Structure representing a formula.
    :type formula: Dictionary

    :param atom: List of consistent formulas representing an atom of the
        closure.
    :type atom: List of :py:class:`~formula.Formula`.

    :returns: ``True`` if the formula is in atom or ``False`` otherwise.
    :rtype: Boolean

    :Example:

    >>> from tccMChecker.closure import *
    >>> from tccMChecker.model_checking_graph import *
    >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
    >>> closure = []
    >>> get_closure(phi,closure)
    >>> atoms = get_all_atoms(closure)
    >>> is_in_atom({'': 'in=true'}, atoms[0])
    True

    .. seealso::
        :py:func:`closure.getClosure`, :py:class:`formula.Formula`,
        :py:func:`.getAllAtoms`
    """
    for formulaAtom in atom:
        if formulaAtom.get_formula() == formula:
            return True
    return False


def clean_connector(formula):
    formula_temp = formula.get_formula()
    key = formula_temp.keys()[0]
    key_new = key.replace(" ", "")
    formula_temp[key_new] = formula_temp.pop(key)
    return Formula(formula_temp)


def is_consistent(formula, atom):
    """
    Checks if a formula is consistent with the set of formulas in an atom.

    :param formula: Formula
    :type formula: :py:class:`~formula.Formula`

    :param atom: List of consistent formulas representing an atom of the
        closure.
    :type atom: List of :py:class:`~formula.Formula`.

    :returns: ``True`` if the formula is consistent with the set of formulas
        in the atom or ``False`` otherwise.
    :rtype: Boolean

    :Example:

    >>> from tccMChecker.closure import *
    >>> from tccMChecker.model_checking_graph import *
    >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
    >>> closure = []
    >>> get_closure(phi,closure)
    >>> atoms = get_all_atoms(closure)
    >>> is_consistent(Formula({'': 'x=1'}), atoms[0])
    False

    .. seealso::
        :py:func:`closure.getClosure`, :py:class:`formula.Formula`,
        :py:func:`.getAllAtoms`

    .. note::

        This function is based on the conditions shown in the definition 6.1
        of the thesis document.
    """
    formula = clean_connector(formula)
    print("verifying: ", formula.get_formula())

    if not is_in_atom(formula.get_negation().get_formula(), atom):
        if formula.get_connective() == "<>":  # <> rules
            if is_in_atom({"o": formula.get_formula()}, atom) or \
                    is_consistent(Formula(formula.get_values()), atom):
                return True

        elif formula.get_connective() == "[]":  # [] rules
            if is_in_atom({"o": formula.get_formula()}, atom) and \
                    is_consistent(Formula(formula.get_values()), atom):
                return True

        elif formula.get_connective() == "^":  # ^ rules
            subformulas = formula.get_subformulas()
            if is_consistent(subformulas[0], atom) and \
                    is_consistent(subformulas[1], atom):
                return True

        elif formula.get_connective() == "v":  # v rules
            subformulas = formula.get_subformulas()
            if is_consistent(subformulas[0], atom) or \
                    is_consistent(subformulas[1], atom):
                return True

        elif formula.is_proposition() or formula.get_connective() == "o" or \
                formula.is_negative_next():
            if formula.is_proposition() and formula.get_connective() == "":
                if proposition_consistent(formula, atom):
                    return True

            elif formula.is_proposition() and formula.get_connective() == "~":
                print("it is not the negation")
                return True

            elif formula.get_formula().keys()[0] == " ":  # when {" ": values}
                if is_in_atom({"": formula.get_formula().values()[0]}, atom):
                    return True

            elif is_in_atom(formula.get_formula(), atom):
                return True

    return False


def delete_atoms(atoms, index_list):
    """
    Removes atoms from a list of atoms.

    :param atoms: List of atoms.
    :type atoms: List of lists

    :param index_list: Index list of the elements to be removed.
    :type index_list: List

    :returns: List of atoms with atoms removed.
    :rtype: List.

    :Example:

    >>> from tccMChecker.closure import *
    >>> from tccMChecker.model_checking_graph import *
    >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
    >>> closure = []
    >>> get_closure(phi,closure)
    >>> atoms = get_all_atoms(closure)
    >>> len(atoms)
    16
    >>> newAtoms = delete_atoms(atoms,[0,2,3,4,5,6,7,8,9,10,11,12,14,15])
    >>> len(newAtoms)
    2

    .. seealso::
        :py:func:`closure.getClosure`, :py:class:`formula.Formula`,
        :py:func:`.getAllAtoms`
    """
    result = []
    index = 0
    while index < len(atoms):
        if index in index_list:
            result.insert(0, atoms[index])
        else:
            result.append(atoms[index])
        index += 1
    return result[len(index_list):]


def proposition_consistent(formula, atom):
    """
    Checks if a proposition is consistent with the formulas of an atom.

    :param formula: Formula
    :type formula: :py:class:`~formula.Formula`

    :param atom: Atom
    :type atom: List of :py:class:`~formula.Formula`

    :returns: ``True`` if the proposition is consistent with the atom or
        ``False`` otherwise.
    :rtype: Boolean.

    :Example:

    >>> from tccMChecker.closure import *
    >>> from tccMChecker.model_checking_graph import *
    >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
    >>> closure = []
    >>> get_closure(phi,closure)
    >>> atoms = get_all_atoms(closure)
    >>> proposition = Formula({"~":"x=2"})
    >>> atom = atoms[0]
    >>> for formula in atom:
    ...     print(formula.get_formula())
    ...
    {'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}
    {'': 'in=true'}
    {'o': 'x=2'}
    {'': 'x=2'}
    {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
    {'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
    >>> proposition_consistent(proposition, atom)
    False

    .. seealso::
        :py:func:`closure.getClosure`, :py:class:`formula.Formula`,
        :py:func:`.getAllAtoms`
        
    """
    print("it is a proposition")
    if formula.is_proposition() and (
                formula.get_values() in formula.get_proposition_rules().keys()):
        no_consistent_propositions = formula.get_consistent_propositions()
        for no_consistent_proposition in no_consistent_propositions:
            if is_in_atom(no_consistent_proposition, atom):
                print("by", no_consistent_proposition)
                return False
        print("There are no inconsistencies, then it is consistent")
        return True
    return False


def list2dict(lists, offset):
    """
    Converts a list to a dictionary with ascending numbers as keys.

    :param lists: List with elements.
    :type lists: List

    :param offset: Offset of numeration.
    :type offset: Integer

    :returns: Dictionary with numbers as keys, and elements of the list as
        values.
    :rtype: Dictionary.

    :Example:

    >>> from tccMChecker.model_checking_graph import *
    >>> list = ["I", "Love", "Computer", "Science"]
    >>> list2dict(list, 2)
    {2: 'I', 3: 'Love', 4: 'Computer', 5: 'Science'}
         
    """
    result = {}
    for index, element in enumerate(lists):
        result[index + offset] = element
    return result


def get_total_nodes(graph):
    """
    Returns the total number of atoms.

    :param graph: Dictionary representing the atoms in each tcc state.
    :type graph: Dictionary

    :returns: The total number of atoms.
    :rtype: Integer

    :Example:

    >>> from tccMChecker.model_checking_graph import *
    >>>> graph = {1: [[Formula({'': 'in=true'}), Formula({'o': 'x=2'})],
    ... [Formula({'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}})]],
    ... 2: [[Formula({'~': 'in=true'}),Formula({'~': {'o': 'x=2'}})]]}
    >>> get_total_nodes(graph)
    3

    .. seealso::
        :py:class:`formula.Formula`
        
    """
    total = 0
    for index_node in graph.keys():
        total += len(graph.get(index_node))
    return total


def get_model_checking_atoms(tcc_structure, atoms):
    """
    Returns the atoms corresponding to the states of a tcc structure.

    :param tcc_structure: Structure representing the behaviour of a system.
    :type tcc_structure: Dictionary

    :param atoms: List of all possible atoms of closure.
    :type atoms: List of atoms

    :returns: Dictionary that have the states of a tcc structure as keys, and a
        list of consistent atoms as values.
    :rtype: Dictionary

    :Example:

    >>> from tccMChecker.model_checking_graph import *
    >>> from tccMChecker.closure import *
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
    >>> get_closure(phi,closure)
    >>> atoms = get_all_atoms(closure)
    >>> model_checking_atoms = get_model_checking_atoms(tcc_structure,atoms)
    >>> for tcc_node in model_checking_atoms.keys():
    ...     print("tcc State", tcc_node)
    ...     tcc_atoms = model_checking_atoms.get(tcc_node)
    ...     for atom_index in tcc_atoms.keys():
    ...             print("Atom ", atom_index)
    ...             for formula in tcc_atoms.get(atom_index):
    ...                     (formula.get_formula(), " | ",)
    ...             print("\\n")
    tcc State 1
    Atom  1
    {'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}  |  {'': 'in=true'}  |  {'o': 'x=2'}  |  {'': 'x=2'}  |  {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}  |  {'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}  |
    Atom  2
    {'~': {'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}}  |  {'': 'in=true'}  |  {'o': 'x=2'}  |  {'': 'x=2'}  |  {'o': {'~': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}}  |  {'~': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}  |  {'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}  |

    .. seealso::
        :py:func:`closure.getClosure`, :py:class:`formula.Formula`,
        :py:func:`.getAllAtoms`
    """
    model_checking_atoms = {}
    for tcc_node in tcc_structure.keys():
        print("looking for proposition of the state {} of {}".format(
            tcc_node, tcc_structure.keys()))
        atoms_node = copy.deepcopy(atoms)
        propositions = tcc_structure.get(tcc_node).get("store")

        for proposition in propositions:  # Propositions as formulas
            index_atom = 0
            l_delete_atoms = []

            while index_atom < len(atoms_node):
                atom = atoms_node[index_atom]

                print("-------------------------------------------------------")
                print("evaluating proposition: ", proposition.get_formula())
                for f in atom:
                    print(f.get_formula())

                if is_consistent(proposition, atom):
                    print("it is consistent")

                    if proposition.get_connective() == "^":
                        subformulas = proposition.get_subformulas()

                        if not is_in_atom(subformulas[0].get_formula(), atom):
                            atoms_node[index_atom].append(
                                clean_connector(subformulas[0]))

                        if not is_in_atom(subformulas[1].get_formula(), atom):
                            atoms_node[index_atom].append(
                                clean_connector(subformulas[1]))

                    if not is_in_atom(proposition.get_formula(), atom):
                        atoms_node[index_atom].append(proposition)
                else:
                    print("it is not consistent")
                    l_delete_atoms.append(index_atom)

                index_atom += 1

            atoms_node = delete_atoms(atoms_node, l_delete_atoms)

        model_checking_atoms[tcc_node] = list2dict(
            atoms_node, get_total_nodes(model_checking_atoms) + 1)

    return model_checking_atoms


def is_next_state(next_formulas, next_atom):
    r"""
    Checks if an atom satisfies a list of formulas with next operator as main
    connective.

    :param next_formulas: List of formulas with next operator as main
        connective.
    :type next_formulas: List of :py:class:`~formula.Formula`

    :param next_atom: Atom.
    :type next_atom: List of :py:class:`~formula.Formula`

    :returns: ``True`` if the atom satisfies the temporal formulas or ``False``
        otherwise.
    :rtype: Boolean

    :Example:

    >>> from tccMChecker.model_checking_graph import *
    >>> atom = [Formula({'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}),
    ... Formula({'': 'in=true'}), Formula({'o': 'x=2'}), Formula({'': 'x=2'}),
    ... Formula({'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}),
    ... Formula({'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}})]
    >>>
    >>> formulas = [Formula({'o': 'x=2'})]
    >>> is_next_state(formulas,atom)
    True

    .. note::
        We say that an atom satisfies a list of formulas when for all the
        formulas :math:`\circ\phi` in the list we found a formula :math:`\phi`
        in the atom.

    .. seealso::
        :py:class:`formula.Formula`

    """
    for formula in next_formulas:
        next = Formula(formula.get_values())
        if not is_in_atom(next.get_formula(), next_atom):
            return False
    return True


def get_model_checking__graph(tcc_structure, model_checking_atoms):
    """
    Returns the model checking graph

    :param tcc_structure: Structure representing the behavior of a system.
    :type tcc_structure: Dictionary

    :param model_checking_atoms: Atoms of a tcc structure.
    :type model_checking_atoms: Dictionary

    :returns: Structure representing the model checking graph.
    :rtype: Dictionary

    :Example:

    >>> from tccMChecker.model_checking_graph import *
    >>> from tccMChecker.closure import *
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
    >>> get_closure(phi,closure)
    >>> atoms = get_all_atoms(closure)
    >>> model_checking_atoms = get_model_checking_atoms(tcc_structure,atoms)
    >>> get_model_checking__graph(tcc_structure, model_checking_atoms)
    {1: [9, 11, 12, 13, 15], 2: [10, 16, 14], 3: [], 4: [], 5: [9, 11, 12, 13, 15], 6: [10, 16, 14], 7: [], 8: [], 9: [9, 11, 12, 13, 15], 10: [10, 16, 14], 11: [], 12: [], 13: [], 14: [], 15: [25, 27, 28, 29, 31], 16: [26, 32, 30], 17: [], 18: [], 19: [25, 27, 28, 29, 31], 20: [26, 32, 30], 21: [], 22: [], 23: [25, 27, 28, 29, 31], 24: [26, 32, 30], 25: [9, 11, 12, 13, 15], 26: [10, 16, 14], 27: [], 28: [], 29: [], 30: [], 31: [25, 27, 28, 29, 31], 32: [26, 32, 30]}

    .. figure:: ./img/example_model_checking_graph.png
        :align: center
        :height: 400px

        Model checking graph generated.

    .. seealso::
        :py:func:`closure.getClosure`, :py:class:`formula.Formula`,
        :py:func:`.getAllAtoms`
    """
    model_checking_graph = {}
    for tcc_node in tcc_structure.keys():
        atoms_tcc_node = model_checking_atoms.get(tcc_node)

        for index_n1 in atoms_tcc_node.keys():
            atom_n1 = atoms_tcc_node.get(index_n1)
            next_formulas = search_formulas(atom_n1, "o")
            next_nodes = []

            for next_tcc_node in tcc_structure[tcc_node].get("edges"):
                atoms_next_tcc_node = model_checking_atoms.get(next_tcc_node)
                for index_n2 in atoms_next_tcc_node.keys():
                    atom_n2 = atoms_next_tcc_node.get(index_n2)
                    if is_next_state(next_formulas, atom_n2):
                        next_nodes.append(index_n2)
            model_checking_graph[index_n1] = next_nodes
    return model_checking_graph
