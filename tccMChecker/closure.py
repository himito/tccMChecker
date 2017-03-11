"""This module contains the functions necessary to generate the closure of a
temporal formula"""

from __future__ import print_function

from formula import Formula


def get_closure(formula, closure):
    """ 
    Function that generates the closure of a temporal formula.
    
    :param formula: Temporal formula that we want to find the closure 
    :param closure: Empty list to store the subformulas of the closure
    :type formula: Formula
    :type closure: List
    
    :Example:
    
    >>> from tccMChecker.closure import *
    >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
    >>> closure = []
    >>> get_closure(phi,closure)
    >>> for formula in closure:
    ...     print(formula.get_formula())
    ...
    {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
    {'~': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}
    {'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}
    {'~': {'o': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}}
    {'o': {'~': {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}}}
    {'^': {'': 'in=true', '~': {'o': 'x=2'}}}
    {'~': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
    {'': 'in=true'}
    {'~': 'in=true'}
    {'o': 'x=2'}
    {'~': {'o': 'x=2'}}
    {'o': {'~': 'x=2'}}
    {'': 'x=2'}
    {'~': 'x=2'}
    
    .. note::
    
        This function is based on the conditions shown in the section 6.1 of the
        thesis document.
    """

    if formula.is_negative_formula():
        formula = Formula(formula.get_values())

    subformula = formula.get_values()

    if formula.is_proposition():  # PROPOSITION rule
        closure.append(Formula({"": subformula}))  # p
        closure.append(Formula({"~": subformula}))  # ~p

    elif formula.get_connective() == "^":  # AND rule
        subformulas = formula.get_subformulas()
        closure.append(Formula({"^": subformula}))  # phi ^ psi
        closure.append(Formula({"~": {"^": subformula}}))  # ~ (phi ^ psi)
        get_closure(subformulas[0], closure)
        get_closure(subformulas[1], closure)

    elif formula.get_connective() == "v":  # OR rule
        subformulas = formula.get_subformulas()
        closure.append(Formula({"v": subformula}))  # phi v psi
        closure.append(Formula({"~": {"v": subformula}}))  # ~ (phi v psi)
        get_closure(subformulas[0], closure)
        get_closure(subformulas[1], closure)

    elif formula.get_connective() == "o":  # NEXT rule
        closure.append(Formula({"o": subformula}))  # o phi
        closure.append(Formula({"~": {"o": subformula}}))  # ~o phi
        closure.append(Formula({"o": {"~": subformula}}))  # o~ phi
        get_closure(Formula(formula.get_values()), closure)

    elif formula.get_connective() == "<>":  # FUTURE rule
        closure.append(Formula({"<>": subformula}))  # <> phi
        closure.append(Formula({"~": {"<>": subformula}}))  # ~<> phi
        closure.append(Formula({"o": {"<>": subformula}}))  # o<> phi
        closure.append(Formula({"~": {"o": {"<>": subformula}}}))  # ~o<> phi
        closure.append(Formula({"o": {"~": {"<>": subformula}}}))  # o~<> phi
        get_closure(Formula(formula.get_values()), closure)

    elif formula.get_connective() == "[]":  # GLOBALLY rule
        closure.append(Formula({"[]": subformula}))  # [] phi
        closure.append(Formula({"~": {"[]": subformula}}))  # ~[] phi
        closure.append(Formula({"o": {"[]": subformula}}))  # o[] phi
        closure.append(Formula({"~": {"o": {"[]": subformula}}}))  # ~o[] phi
        closure.append(Formula({"o": {"~": {"[]": subformula}}}))  # o~[] phi
        get_closure(Formula(formula.get_values()), closure)
