#!/usr/bin/python3

import itertools

# NOTE: This is very much the same as a previous exercise's logic.py.
# The new features we need for reducing the quantifiers forall, forsome
# and exactlyone to propositional logic is the 'map' method, which
# makes maps a formula to another one with otherwise exactly the same
# structure except that the atomic formulas have been replaced by
# something else, as expressed by the function M. The cases for
# ATOM, TRUE and FALSE are implemented, and your task is to
# do the implementation for AND, OR, and NOT.

# Representation of propositional formulas in Python.
#
# The basic connectives are NOT, AND and OR.
# IMPL and EQVI are reduced to these through the obvious reductions.
# We have a separate class for formulas with different outermost
# connectives, as well as for atomic formulas (ATOM).
#
# The methods supported are:
#   negin(self)    Negation of formula; negation pushed in one level (if possible)
#   clauses(self)  Return clauses representing the formula
#   vars(self)     Return variables occurring in a formula
#   map(self,M)    Maps the formula to a new one with atoms x replaced by formula M(x)
#

# Translation to CNF:
# Instead of applying the logical equivalences to incrementally transform
# a formula to CNF, the 'clauses' methods below perform a recursive
# transformation to sets of clauses for each formula type after
# the subformulas have been translated into clauses.
# The translations for ATOM, NOT(ATOM ...), and AND(...) are trivial.
# The complicated part is the translation for OR after its subformulas
# have been translated to clauses, i.e. computing the disjunction
# of two or more clause sets.

# auxiliary functions
def concatlists(ll):
  return list(itertools.chain.from_iterable(ll))

# Both AND and OR will inherit __init__ and vars from NaryFormula
# NaryFormula means formulas with multiple subformulas.
# cCnjunction (AND) and disjunction (OR) are traditionally defined
# as binary connectives, that is, with two subformulas.
# Because of associativity, ie. A & (B & C) and (A & B) & C are equivalent,
# it is often more convenient to write A & B & C.

class NaryFormula: # N-ary formulas with multiple subformulas
  def __init__(self,subformulas):
    self.subformulas = subformulas
  def vars(self):
    vs = [ f.vars() for f in self.subformulas ]
    return set.union(*vs)

class BinaryFormula: # Not used here
  def __init__(self,subformula1,subformula2):
    self.subformula1 = subformula1
    self.subformula2 = subformula2

# AND and OR are defined with multiple subformulas (phi1 & phi2 & ... & phiN)

class AND(NaryFormula):
  def __repr__(self):
    return "(and " + (' '.join([ str(x) for x in self.subformulas])) + ")"
  def negin(self):
    return OR([ NOT(f) for f in self.subformulas ])
  def clauses(self):
    return concatlists([ c.clauses() for c in self.subformulas ])
  def map(self,M):
    return AND([c.map(M) for c in self.subformulas])
#### IMPLEMENT MISSING CODE HERE ####
#### IMPLEMENT MISSING CODE HERE ####

class OR(NaryFormula):
  def __repr__(self):
    return "(or " + (' '.join([ str(x) for x in self.subformulas])) + ")"
  def negin(self):
    return AND([ NOT(f) for f in self.subformulas ])
  def clauses(self):
    cclauses = [ c.clauses() for c in self.subformulas ]
    return [ concatlists(list(c)) for c in itertools.product(*cclauses) ]
  def map(self,M):
    return OR([c.map(M) for c in self.subformulas])
#### IMPLEMENT MISSING CODE HERE ####
#### IMPLEMENT MISSING CODE HERE ####

class NOT:
  def __init__(self,subformula):
    self.subformula = subformula
  def __repr__(self):
    return "(not " + str(self.subformula) + ")"
  def negin(self):
    return self.subformula
  def clauses(self):
    if isinstance(self.subformula,ATOM):
      return [[(self.subformula.name,False)]]
    else:
      negsubformula = self.subformula.negin()
      return negsubformula.clauses()
  def vars(self):
    return self.subformula.vars()
  def map(self,M):
    return NOT(self.subformula.map(M))
#### IMPLEMENT MISSING CODE HERE ####
#### IMPLEMENT MISSING CODE HERE ####

class ATOM:
  def __init__(self,name):
    self.name = name
  def __repr__(self):
    return str(self.name)
  def negin(self):
    return NOT(self)
  def clauses(self):
    return [[(self.name,True)]]
  def vars(self):
    return { self.name }
  def map(self,M):
    return M(self.name)

class TRUE:
  def __repr__(self):
    return "true"
  def negin(self):
    return FALSE()
  def clauses(self):
    return []
  def vars(self):
    return set()
  def map(self,M):
    return self
      
class FALSE:
  def __repr__(self):
    return "false"
  def negin(self):
    return TRUE()
  def clauses(self):
    return [[]]
  def vars(self):
    return set()
  def map(self,M):
    return self
      
    
# Implication and equivalence reduced to the primitive connectives

# A -> B is reduced to -A V B

def IMPL(f1,f2):
  return OR([NOT(f1),f2])

# A <-> B is reduced to (-A V B) & (-B V A)

def EQVI(f1,f2):
  return AND([IMPL(f1,f2),IMPL(f2,f1)])
