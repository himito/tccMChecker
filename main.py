# -*- coding: utf-8 -*-

# Codification:
# <> : Sometimes
# [] : Always
# ~ : Negation
# v : or
# o : next
# ^ : and


class Formula:
	prepositions = ["in=true", "x=2", "x=1"]
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
	
	def getSubFormulas(self):
		subformulas = []
		newFormula = self.getValues()
		connectives = newFormula.keys()
		for connective in connectives:
			subformulas.append(Formula({connective : newFormula.get(connective)}))
		return subformulas
	
	def getConnective(self):
		return self.formula.keys()[0]
	
	def isPreposition(self):
		if len(self.formula) == 1 and (self.getConnective() not in self.operators[:-1]):
			return self.formula.values()[0] in self.prepositions
		return False
	
	def isNegativeFormula(self):
		subformula = Formula(self.getValues())
		if (self.getConnective() == "~" and (subformula.getConnective() in self.operators[:-1])):
			return True
		return False


def getClosure(formula, closure):

	if formula.isNegativeFormula():
		formula = Formula(formula.getValues())
	
	subformula = formula.getValues()
	
	if formula.isPreposition(): # Preposition rule
		closure.append(Formula({"": subformula})) # p
		closure.append(Formula({"~": subformula})) # ~p
	
	elif formula.getConnective() == "^" : # And rule
		subformulas = formula.getSubFormulas()
		closure.append(Formula({"^": subformula})) # phi ^ psi
		closure.append(Formula({"~": {"^": subformula}})) # ~ (phi ^ psi)
		getClosure(subformulas[0],closure)
		getClosure(subformulas[1],closure)
	
	elif formula.getConnective() == "v" : # Or rule
		subformulas = formula.getSubFormulas()
		closure.append(Formula({"v": subformula})) # phi v psi
		closure.append(Formula({"~": {"v": subformula}})) # ~ (phi v psi)
		getClosure(subformulas[0],closure)
		getClosure(subformulas[1],closure)
		
	elif formula.getConnective() == "o" : # Or rule
		closure.append(Formula({"o": subformula})) # o phi
		closure.append(Formula({"~": {"o": subformula}})) # ~o phi
		closure.append(Formula({"o": {"~": subformula}})) # o~ phi
		getClosure(Formula(formula.getValues()),closure)
			
	elif formula.getConnective() == "<>": # Diamond rule
		closure.append(Formula({"<>": subformula})) # <> phi
		closure.append(Formula({"~": {"<>": subformula}})) # ~<> phi
		closure.append(Formula({"o": {"<>": subformula}})) # o<> phi
		closure.append(Formula({"~": {"o": {"<>": subformula}}})) # ~o<> phi
		closure.append(Formula({"o": {"~": {"<>": subformula}}})) # o~<> phi
		getClosure(Formula(formula.getValues()),closure)

	elif formula.getConnective() == "[]": # Diamond rule
		closure.append(Formula({"[]": subformula})) # [] phi
		closure.append(Formula({"~": {"[]": subformula}})) # ~[] phi
		closure.append(Formula({"o": {"[]": subformula}})) # o[] phi
		closure.append(Formula({"~": {"o": {"[]": subformula}}})) # ~o[] phi
		closure.append(Formula({"o": {"~": {"[]": subformula}}})) # o~[] phi
		getClosure(Formula(formula.getValues()),closure)

closure = []
phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
# phi = Formula({"^":{"":"in=true","~":{"o":"x=2"}}})
# phi = Formula({"":"in=true"})
# phi = Formula({"~":{"o":"x=2"}})
# phi = Formula({"o":"x=2"})
# phi = Formula({"":"x=2"})

print "Formula: "
print phi.formula

getClosure(phi,closure)
print "Clausura: ", len(closure)
for formula in closure:
	print formula.formula




