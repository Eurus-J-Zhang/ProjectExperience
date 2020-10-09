#!/usr/bin/python3

# 2020 (C) Aalto University, Jussi Rintanen

import time
import itertools

import logic

################ Davis-Putnam-Logemann-Loveland procedure ############

### Unit propagation
#
# Got through all clauses (until no change takes place).
# If clause has no True literals and all literals except one
# are False, then the remaining literal must be made True.
# Otherwise (if that literal was False), the whole clause set
# would be false.

def unitpropagate(V,clauses):
  # Keep track of variables that were assigned a new values
  assvars = set()
  change = False
  # Inferences for one clause
  def doClause(c):
    cntFalse = 0
    for (v,tf) in c:
      if not v in V: # Variable without value
        candv = v
        candval = tf
      else:
        val = V[v]
        if val == tf: # Literal is True, do nothing
          return True
        cntFalse = cntFalse + 1 # Count number of False literals
    if cntFalse == len(c): # All literals are False
      return False
    if cntFalse+1 == len(c): # Exactly one literal un-assigned
      V[candv] = candval # Assign the value it must have
      assvars.add(candv)
      change = True
    return True
  # Make inferences with every clause
  change = True
  while change: # Go through clause set as long as new values are inferred
    change = False
    for c in clauses:
      if doClause(c) == False: # Clause False, so whole clause set is False
        return (False,assvars)
  return (True,assvars)

### DPLL: The Davis-Putnam-Logemann-Loveland procedure
#
# The most basic way of testing satisfiability is equivalent to the
# truth-table method: exhaustively generate all 2^n valuations with
# a binary tree of depth n, with each leave representing a valuation and
# each inner node representing case analysis on the two possible values
# of a propositional variable.
#
# The Davis-Putnam procedure improves on this by performing Unit Propagation
# after each case analysis: some variable must have a certain value, because
# otherwise one of the clauses would be false, and instead of doing a case
# analysis on that variable, we will assign the forced value to the variable.
#
# What Unit Propagation does is to identify clauses l1 V l2 V ... V Ln
# that does not contain any True literals under the current (partial) valuation,
# and that contains n-1 False literals. The remaining literal (which does not
# have a value) must be made True, because otherwise the clause and the whole
# clause set would be False. If the literal is positive, assign the variable in
# it True, and otherwise the literal is negative and assign the variable False.
#
# This, relatively simple, improvement makes it possible to solve orders of
# magnitudes harder satisfiability problems than what is possible with the truth-table
# method. Additional improvements in implementation technology (best possible
# data structures, minimization of cache misses etc.) as well as clever ways
# of choosing the variables for case analysis, and many other improvements,
# have lifted the scalability of SAT solving still dramatically further in
# the past 25 years.

decisions = 0

def search(V,allvars,clauses):
  global decisions

  # Perform Unit Propagation to infer new variable values
  result,assvars = unitpropagate(V,clauses)
  # assvars contains variables that were assigned by Unit Propagation
  if result == False:
    for v in assvars: # Undo value assignments at this level
      del V[v]
    return False

  # Choose new variable for case analysis
  branchvar = -1
  for v in allvars:
    if not v in V:
      branchvar = v
      break
  if branchvar == -1: # No unassigned variables left, formula in SAT
    return True
  
  decisions = decisions + 1 # Count number of case analyses

  # Case 1: Try making branchvar True.
  V[branchvar] = True
  if(search(V,allvars,clauses)) == True:
    return True
  
  # Case 2: Did not work out. Try making branchvar False.
  V[branchvar] = False
  if(search(V,allvars,clauses)) == True:
    return True
  
  # Did not work out. Undo all variable assignments and return False.
  del V[branchvar]
  for v in assvars: # Undo value assignments at this level
    del V[v]
  return False

### Main function

def SAT(fma):
  global decisions
  starttime = time.process_time()

  # Transform the formula to clauses

  clauses = fma.clauses()

  if [] in clauses:
    print("Input contains an empty clause: unsatisfiable")
    return False

  unitclauses = [ c[0] for c in clauses if len(c) == 1 ]
  nonunitclauses = [ c for c in clauses if len(c) > 1 ]

  print(str(len(unitclauses)) + " unit clauses")
  print(str(len(nonunitclauses)) + " longer clauses")
  print(str(max([ len(c) for c in clauses])) + " is maximum clause length")

  # BUG: Check for contradictory unit clauses missing
  # FEATURE: Valid clauses are currently not filtered out
  
  V = { } # Empty dictionary for the empty partial valuation

  # The initial valuation is obtained from unit clauses
  for (v,tf) in unitclauses:
    V[v] = tf

  # Unit propagate unit clauses (this part of valuation will not change later!)
  result,assvars = unitpropagate(V,nonunitclauses)
  if result == False:
    print("Initial unit propagation derived a contradiction: unsatisfiable")
    return False

  # Start tree search
  decisions = 0
  if search(V,fma.vars(),nonunitclauses) == True: # Satisfying valuation found
    endtime = time.process_time()
    print("SAT (" + str(decisions) + " decisions)")
    print(str(endtime-starttime) + " seconds")
    return V

  # Search terminated because formula is unsatisfiable
  
  endtime = time.process_time()
  print("UNSAT (" + str(decisions) + " decisions)")
  print(str(endtime-starttime) + " seconds")
  return False
