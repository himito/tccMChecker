"""This module contains the class to describe a temporal formula."""

from __future__ import print_function


class Formula(object):
    r"""This class represents a temporal formula.

    :param data: Structure representing the temporal formula.
    :type data: Dictionary.

    :Example:

    :math:`\phi = \diamondsuit(\mathtt{in=true} \wedge \neg\circ(\mathtt{x=2}))`

    >>> from tccMChecker.formula import *
    >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})

    .. note::
        Logic operators are represented by the following symbols:

        * Globally : ``[]``
        * Future : ``<>``
        * Next : ``o``
        * Negation : ``~``
        * Or : ``v``
        * And : ``^``

    """
    __propositions = ["da=0", "da=5", "da=10", "da=15", "da=20", "b=0", "b=1",
                      "b=2", "b=3", "sm=0", "sm=5", "sm=10", "tc", "tt", "dc",
                      "dd"]
    __proposition_rules = {"da=0": [{"~": "da=0"}, {"": "da=5"}, {"": "da=10"},
                                    {"": "da=15"}, {"": "da=20"}],
                           "da=5": [{"": "da=0"}, {"~": "da=5"}, {"": "da=10"},
                                    {"": "da=15"}, {"": "da=20"}],
                           "da=10": [{"": "da=0"}, {"": "da=5"}, {"~": "da=10"},
                                     {"": "da=15"}, {"": "da=20"}],
                           "da=15": [{"": "da=0"}, {"": "da=5"}, {"": "da=10"},
                                     {"~": "da=15"}, {"": "da=20"}],
                           "da=20": [{"": "da=0"}, {"": "da=5"}, {"": "da=10"},
                                     {"": "da=15"}, {"~": "da=20"}],
                           "b=0": [{"~": "b=0"}, {"": "b=1"}, {"": "b=2"},
                                   {"": "b=3"}],
                           "b=1": [{"": "b=0"}, {"~": "b=1"}, {"": "b=2"},
                                   {"": "b=3"}],
                           "b=2": [{"": "b=0"}, {"": "b=1"}, {"~": "b=2"},
                                   {"": "b=3"}],
                           "b=3": [{"": "b=0"}, {"": "b=1"}, {"": "b=2"},
                                   {"~": "b=3"}],
                           "sm=0": [{"~": "sm=0"}, {"": "sm=5"}, {"": "sm=10"}],
                           "sm=5": [{"": "sm=0"}, {"~": "sm=5"}, {"": "sm=10"}],
                           "sm=10": [{"": "sm=0"}, {"": "sm=5"},
                                     {"~": "sm=10"}],
                           "tc": [{"~": "tc"}],
                           "tt": [{"~": "tt"}],
                           "dc": [{"~": "dc"}],
                           "dd": [{"~": "dd"}],
                           }
    __operators = ["o", "<>", "[]", "v", "^", "~"]
    __formula = {}

    def __init__(self, data):
        """
        Constructor method.

        :param data: Structure representing the temporal formula.
        :type data: Dictionary.

        """
        if type(data) == str:
            self.__formula = {"": data}
        else:
            self.__formula = data

    def get_consistent_propositions(self):
        r"""
        Returns the consistent propositions of a formula.

        :returns: A structure representing the consistent proposition of the
            formula.
        :rtype: Dictionary.

        :Example:

        :math:`\phi = (x = 2) \hspace{2cm} consistentPropositions(\phi) = \neg(x=1)`

        >>> from tccMChecker.formula import *
        >>> phi = Formula({"": "x=2"})
        >>> phi.get_consistent_propositions()
        {'~': 'x=1'}

        """
        return self.__proposition_rules.get(self.get_values())

    def get_formula(self):
        """
        Returns the formula.

        :returns: A structure representing the formula.
        :rtype: Dictionary.

        :Example:

        >>> from tccMChecker.formula import *
        >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
        >>> phi.get_formula()
        {'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}

        """
        return self.__formula

    def get_proposition_rules(self):
        """
        Returns the consistent propositions of all propositions in the
        implementation.

        :Example:

        :returns: A dictionary containing as key a proposition, and value all
            possible propositions that are consistent.
        :rtype: Dictionary.

        >>> from tccMChecker.formula import *
        >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
        >>> phi.get_proposition_rules()
        {'x=1': {'~': 'x=2'}, 'x=2': {'~': 'x=1'}}

        """
        return self.__proposition_rules

    def get_values(self):
        r"""
        Returns the formula without the outermost unary operator.

        :returns: A structure representing the formula without the outermost
            unary operator.
        :rtype: Dictionary

        :Example:

        :math:`{\tiny \phi = \diamondsuit(\mathtt{in=true} \wedge \neg\circ(\mathtt{x=2})) \hspace{1cm} getValues(\phi) = (\mathtt{in=true}) \wedge \neg\circ(\mathtt{x=2})}`

        >>> from tccMChecker.formula import *
        >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
        >>> phi.get_values()
        {'^': {'': 'in=true', '~': {'o': 'x=2'}}}

        """
        return self.__formula.values()[0]

    def get_negation(self):
        r"""
        Returns the negation of the formula.

        :returns: The negation of the formula.
        :rtype: :py:class:`~formula.Formula`.

        :Example:

        :math:`\phi = \circ(\mathtt{x=2}) \hspace{2cm} \neg\phi = \neg\circ(\mathtt{x=2})`

        >>> from tccMChecker.formula import *
        >>> phi = Formula({"o":"x=2"})
        >>> negPhi = phi.get_negation()
        >>> negPhi.get_formula()
        {'~': {'o': 'x=2'}}

        """
        if self.get_connective() == "~":
            if self.is_proposition():
                return Formula({"": self.get_values()})
            else:
                return Formula(self.get_values())
        elif self.is_proposition():
            return Formula({"~": self.get_values()})
        else:
            return Formula({"~": self.__formula})

    def get_subformulas(self):
        r"""
        Returns the subformulas attached to a binary operator.

        :returns: A list containing the subformulas.
        :rtype: List.

        :Example:

        :math:`\alpha = (\mathtt{in=true}) \wedge \neg\circ(\mathtt{x=2}) \hspace{1cm} \phi= (\mathtt{in=true})  \hspace{1cm} \psi= \neg\circ(\mathtt{x=2})`

        >>> from tccMChecker.formula import *
        >>> alpha = Formula({"^":{"":"in=true","~":{"o":"x=2"}}})
        >>> subformulas = alpha.get_subformulas()
        >>> for subformula in subformulas:
        ...     print(subformula.get_formula())
        {'': 'in=true'}
        {'~': {'o': 'x=2'}}

        """
        subformulas = []
        new_formula = self.get_values()
        connectives = new_formula.keys()
        for connective in connectives:
            subformulas.append(
                Formula({connective: new_formula.get(connective)}))
        return subformulas

    def get_connective(self):
        r"""
        Return the main connective of the formula.

        :returns: A string representing the main connective of the formula.
        :rtype: String.

        :Example:

        :math:`\phi = \diamondsuit(\mathtt{in=true} \wedge \neg\circ(\mathtt{x=2})) \hspace{2cm} getConnective(\phi) = \diamondsuit`

        >>> from tccMChecker.formula import *
        >>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
        >>> phi.get_connective()
        '<>'

        """
        return self.__formula.keys()[0]

    def is_proposition(self):
        """
        Checks if the formula is a proposition.

        :returns: ``True`` if the formula is a proposition or ``False``
            otherwise.
        :rtype: Boolean.

        :Example:

        >>> from tccMChecker.formula import *
        >>> phi = Formula({"":"x=2"})
        >>> phi.is_proposition()
        True

        """
        if len(self.__formula) == 1 and (
                    self.get_connective() not in self.__operators[:-1]):
            return self.__formula.values()[0] in self.__propositions
        return False

    def is_negative_next(self):
        r"""
        Checks if the formula is of the form :math:`\neg\circ\phi`.

        :returns: ``True`` if the formula is of the form :math:`\neg\circ\phi`
            or ``False`` otherwise.
        :rtype: Boolean.

        :Example:

        >>> from tccMChecker.formula import *
        >>> phi = Formula({"~": {"o":"x=2"}})
        >>> phi.is_negative_next()
        True

        """
        if self.get_connective() == "~" and type(self.get_values()) != str and \
                        self.get_values().keys()[0] == "o":
            return True
        else:
            return False

    def is_basic(self):
        r"""
        Checks if the formula is a basic formula (i.e. proposition or it has
        :math:`\circ` as main connective)

        :returns: ``True`` if the formula is a basic formula or ``False``
            otherwise.
        :rtype: Boolean.

        :Example:

        >>> from tccMChecker.formula import *
        >>> phi = Formula({"o":"x=2"})
        >>> phi.is_basic()
        True

        """
        if self.get_connective() != "~" and \
                (self.is_proposition() or self.get_connective() == "o"):
            if self.get_connective() == "o" and type(self.get_values()) != str \
                    and self.get_values().keys()[0] == "~":
                return False
            return True
        return False

    def is_negative_formula(self):
        r"""
        Returns if the formula has :math:`\neg` as main connective.

        :returns: ``True`` if the formula has :math:`\neg` as main connective
            or ``False`` otherwise.
        :rtype: Boolean.

        :Example:

        >>> from tccMChecker.formula import *
        >>> phi = Formula({"~":{"o":"x=2"}})
        >>> phi.is_negative_formula()
        True

        """
        subformula = Formula(self.get_values())
        if (self.get_connective() == "~" and
                (subformula.get_connective() in self.__operators[:-1])):
            return True
        return False
