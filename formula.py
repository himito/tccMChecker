# Filename: formula.py

"""
This module contains the class to describe a temporal formula.
"""

__author__ = "Jaime E. Arias Almeida"
__license__ = "beerware"
__version__ = "1.0"
__email__ = "jearias@javerianacali.edu.co"
__docformat__ = 'reStructuredText'


class Formula:
	r"""
	
		This class represents a temporal formula.
		
		:param data: Structure representing the temporal formula.
		:type data: Dictionary.
		
		:Example:
		
		:math:`\phi = \diamondsuit(\mathtt{in=true} \wedge \neg\circ(\mathtt{x=2}))`
		
		>>> from formula import *
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
	__propositions = ["in=true", "x=2", "x=1"]
	__proposition_rules = {"x=2" : {"~":"x=1"}, "x=1" : {"~":"x=2"}}
	__operators = ["o", "<>", "[]", "v", "^", "~"]
	__formula = {}
	
	def __init__(self, data):
		"""
			Constructor method.
			
			:param data: Structure representing the temporal formula.
			:type data: Dictionary.
			
		"""
		if (type(data) == str):
			self.__formula = {"": data}
		else:
			self.__formula = data
	
	def getConsistentPropositions(self):
		r"""
			Returns the consistent propositions of a formula.

			:returns: A structure representing the consistent proposition of the formula.
			:rtype: Dictionary.

			:Example:
			
			:math:`\phi = (x = 2) \hspace{2cm} consistentPropositions(\phi) = \neg(x=1)`
			
			>>> from formula import *
			>>> phi = Formula({"": "x=2"})
			>>> phi.getConsistentPropositions()
			{'~': 'x=1'}
			
		"""
		return self.__proposition_rules.get(self.getValues())
		
	def getFormula(self):
		"""
			Returns the formula.
			
			:returns: A structure representing the formula.
			:rtype: Dictionary.

			:Example:
			
			>>> from formula import *
			>>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
			>>> phi.getFormula()
			{'<>': {'^': {'': 'in=true', '~': {'o': 'x=2'}}}}
			
		"""
		return self.__formula
		
	def getPropositionRules(self):
		"""
			Returns the consistent propositions of all propositions in the implementation.
			
			:Example:
			
			:returns: A dictionary containing as key a proposition, and value all possible propositions that are consistent.
			:rtype: Dictionary.

			>>> from formula import *
			>>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
			>>> phi.getPropositionRules()
			{'x=1': {'~': 'x=2'}, 'x=2': {'~': 'x=1'}}
			
		"""
		return self.__proposition_rules
	
	def getValues(self):
		r"""
			Returns the formula without the outermost unary operator.
			
			:returns: A structure representing the formula without the outermost unary operator.
			:rtype: Dictionary

			:Example:
			
			:math:`{\tiny \phi = \diamondsuit(\mathtt{in=true} \wedge \neg\circ(\mathtt{x=2})) \hspace{1cm} getValues(\phi) = (\mathtt{in=true}) \wedge \neg\circ(\mathtt{x=2})}`
			
			>>> from formula import *
			>>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
			>>> phi.getValues()
			{'^': {'': 'in=true', '~': {'o': 'x=2'}}}
					
		"""
		return self.__formula.values()[0]
	
	def getNegation(self):
		r"""
			Returns the negation of the formula.

			:returns: The negation of the formula.
			:rtype: :py:class:`~formula.Formula`.

			:Example:

			:math:`\phi = \circ(\mathtt{x=2}) \hspace{2cm} \neg\phi = \neg\circ(\mathtt{x=2})`

			>>> from formula import *
			>>> phi = Formula({"o":"x=2"})
			>>> negPhi = phi.getNegation()
			>>> negPhi.getFormula()
			{'~': {'o': 'x=2'}}

		"""
		if self.getConnective() == "~":
			if self.isProposition():
				return Formula({"": self.getValues()})
			else:
				return Formula(self.getValues())
		elif self.isProposition():
			return Formula({"~": self.getValues()})
		else:
			return Formula({"~": self.__formula})
	
	def getSubFormulas(self):
		r"""
			Returns the subformulas attached to a binary operator.

			:returns: A list containing the subformulas.
			:rtype: List.

			:Example:

			:math:`\alpha = (\mathtt{in=true}) \wedge \neg\circ(\mathtt{x=2}) \hspace{1cm} \phi= (\mathtt{in=true})  \hspace{1cm} \psi= \neg\circ(\mathtt{x=2})` 

			>>> from formula import *
			>>> alpha = Formula({"^":{"":"in=true","~":{"o":"x=2"}}})
			>>> subformulas = alpha.getSubFormulas()
			>>> for subformula in subformulas:
			...     print subformula.getFormula()
			{'': 'in=true'}
			{'~': {'o': 'x=2'}}

		"""
		subformulas = []
		newFormula = self.getValues()
		connectives = newFormula.keys()
		for connective in connectives:
			subformulas.append(Formula({connective : newFormula.get(connective)}))
		return subformulas
	
	def getConnective(self):
		r"""
			Return the main connective of the formula.

			:returns: A string representing the main connective of the formula.
			:rtype: String.

			:Example:

			:math:`\phi = \diamondsuit(\mathtt{in=true} \wedge \neg\circ(\mathtt{x=2})) \hspace{2cm} getConnective(\phi) = \diamondsuit`

			>>> from formula import *
			>>> phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
			>>> phi.getConnective()
			'<>'

		"""
		return self.__formula.keys()[0]
	
	def isProposition(self):
		"""
			Checks if the formula is a proposition.

			:returns: ``True`` if the formula is a proposition or ``False`` otherwise.
			:rtype: Boolean.

			:Example:

			>>> from formula import *
			>>> phi = Formula({"":"x=2"})
			>>> phi.isProposition()
			True

		"""
		if len(self.__formula) == 1 and (self.getConnective() not in self.__operators[:-1]):
			return self.__formula.values()[0] in self.__propositions
		return False
		
	def isNegativeNext(self):
		r"""
			Checks if the formula is of the form :math:`\neg\circ\phi`.

			:returns: ``True`` if the formula is of the form :math:`\neg\circ\phi` or ``False`` otherwise.
			:rtype: Boolean.

			:Example:

			>>> from formula import *
			>>> phi = Formula({"~": {"o":"x=2"}})
			>>> phi.isNegativeNext()
			True

		"""
		if self.getConnective() == "~" and type(self.getValues()) != str and self.getValues().keys()[0] == "o":
			return  True
		else:
			return False
		
	def isBasic(self):
		r"""
			Checks if the formula is a basic formula (i.e. proposition or it has :math:`\circ` as main connective)

			:returns: ``True`` if the formula is a basic formula or ``False`` otherwise.
			:rtype: Boolean.

			:Example:

			>>> from formula import *
			>>> phi = Formula({"o":"x=2"})
			>>> phi.isBasic()
			True

		"""
		if self.getConnective() != "~" and (self.isProposition() or self.getConnective() == "o"):
			if self.getConnective() == "o" and type(self.getValues()) != str and self.getValues().keys()[0] == "~":
				return False
			return True
		return False
		
	
	def isNegativeFormula(self):
		r"""
			Returns if the formula has :math:`\neg` as main connective.

			:returns: ``True`` if the formula has :math:`\neg` as main connective or ``False`` otherwise.
			:rtype: Boolean.
			
			:Example:

			>>> from formula import *
			>>> phi = Formula({"~":{"o":"x=2"}})
			>>> phi.isNegativeFormula()
			True

		"""
		subformula = Formula(self.getValues())
		if (self.getConnective() == "~" and (subformula.getConnective() in self.__operators[:-1])):
			return True
		return False

