# -*- coding: utf-8 -*-

from formula import Formula

# Closure
def getClosure(formula, closure):

	if formula.isNegativeFormula():
		formula = Formula(formula.getValues())
	
	subformula = formula.getValues()
	
	if formula.isProposition(): # Preposition rule
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





###################################### Execution ###################################### 

# closure = []
# phi = Formula({"<>": {"^":{"":"in=true","~":{"o":"x=2"}}}})
# # phi = Formula({"^":{"":"in=true","~":{"o":"x=2"}}})
# # phi = Formula({"":"in=true"})
# # phi = Formula({"~":{"o":"x=2"}})
# # phi = Formula({"o":"x=2"})
# # phi = Formula({"":"x=2"})
# 
# print "Formula: "
# print phi.formula
# 
# getClosure(phi,closure)
# print "Clausura: ", len(closure)
# for formula in closure:
# 	print formula.formula




