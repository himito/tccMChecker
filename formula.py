# -*- coding: utf-8 -*-

# Operators:
# <> : Sometimes
# [] : Always
# ~ : Negation
# v : or
# o : next
# ^ : and

# Formula
class Formula:
	propositions = ["in=true", "x=2", "x=1"]
	operators = ["o", "<>", "[]", "v", "^", "~"]
	formula = {}
	
	def __init__(self, data):
		if (type(data) == str):
			self.formula = {"": data}
		else:
			self.formula = data
		
	def getFormula(self):
		return self.formula
	
	def getValues(self):
		return self.formula.values()[0]
	
	def getNegation(self):
		if self.getConnective() == "~":
			if self.isProposition():
				return Formula({"": self.getValues()})
			else:
				return Formula(self.getValues())
		elif self.isProposition():
			return Formula({"~": self.getValues()})
		else:
			return Formula({"~": self.formula})
	
	def getSubFormulas(self):
		subformulas = []
		newFormula = self.getValues()
		connectives = newFormula.keys()
		for connective in connectives:
			subformulas.append(Formula({connective : newFormula.get(connective)}))
		return subformulas
	
	def getConnective(self):
		return self.formula.keys()[0]
	
	def isProposition(self):
		if len(self.formula) == 1 and (self.getConnective() not in self.operators[:-1]):
			return self.formula.values()[0] in self.propositions
		return False
		
	def isNegativeNext(self):
		if self.getConnective() == "~" and type(self.getValues()) != str and self.getValues().keys()[0] == "o":
			return  True
		else:
			return False
		
	def isBasic(self):
		if self.getConnective() != "~" and (self.isProposition() or self.getConnective() == "o"):
			if self.getConnective() == "o" and type(self.getValues()) != str and self.getValues().keys()[0] == "~":
				return False
			return True
		return False
		
	
	def isNegativeFormula(self):
		subformula = Formula(self.getValues())
		if (self.getConnective() == "~" and (subformula.getConnective() in self.operators[:-1])):
			return True
		return False

