
import random
import numpy as np
from qlearnexamples import *

# The Q-Learning Algorithm

# EXERCISE ASSIGNMENT:
# Implement the Q-learning algorithm for MDPs.
#   The Q-values are represented as a Python dictionary Q[s,a],
# which is a mapping from the state indices s=0..stateMax to
# and actions a to the Q-values.
#
# Choice of actions can be completely random, or, if you are interested,
# you could implement some scheme that prefers better actions, e.g.
# based on Multi-arm Bandit problems (find more about these in the literature:
# this is an optional addition to the programming assignment.)

# OPTIONAL FUNCTIONS:
# You can implement and use the auxiliary functions bestActionFor and execute
# if you want, as auxiliary functions for Qlearning and makePolicy and makeValues.

# bestActionFor chooses the best action for 'state', given Q values
# Tip: You may return -1 if no action is applicable.
def bestActionFor(mdp,state,Q):

    """
    Find the best available action in `Q` given `state`.
    
    Parameters
    ----------
    mdp : GridMDP object (see `qlearnexamples.py`)
    state : int
       In range [0,mdp.stateMax] (inclusive)
    Q : dict {(state,action) : float}
       Q dictionary mapping from state,action pair to score.
    
    Returns
    -------
    int
       Applicable action for `state` yielding the maximum score.

    """

    best_action = 0
    maxvalue = 0
    action_state = False
    for a in mdp.ACTIONS:
        if (state, a) in Q:
            action_state = True
            if Q[state, a] > maxvalue:
                maxvalue = Q[state, a]
                best_action = a

    if not action_state:
        best_action = -1
    return best_action

    ### YOUR CODE HERE

# valueOfBestAction gives the value of best action for 'state'
# Tip: You may, if needed, return a dummy value of 0 or -1 if there are no Q values for the state/best action.
def valueOfBestAction(mdp,state,Q):
    """
    Return value of best available action in `Q` given `state`.
    
    Parameters
    ----------
    mdp : GridMDP object (see `qlearnexamples.py`)
    state : int
       In range [0,mdp.stateMax] (inclusive)
    Q : dict {(state,action) : float}
       Q dictionary mapping from state,action pair to score.

    Returns
    -------
    float
       Maximum Q-value for any applicable action in `state`.
    
    """

    maxvalue = 0

    for a in mdp.ACTIONS:
        if (state, a) in Q:

            if Q[(state, a)] > maxvalue:
                maxvalue = Q[(state, a)]

    return maxvalue

    ### YOUR CODE HERE
    ### YOUR CODE HERE
    ### YOUR CODE HERE



# 'execute' randomly chooses a successor state for state s w.r.t. action a.
# The probability with which is given successor is chosen must respect
# to the probability given by mdp.successors(s,a).
# execute should return a tuple (s2,r), where s2 is the successor state and r is
# the reward that was obtained.

def execute(mdp,s,a):
    """
    Randomly choose a successor state of state `s` given action `a`.

    The probability of the successor state respects the probability of the
    Markov Decision Process.
    
    Parameters
    ----------
    mdp : GridMDP object (see `qlearnexamples.py`)
    s : int
       Start/current state as integer in range [0,mdp.stateMax] (inclusive)
    a : int
       Action as int in GridMDP.ACTIONS (`[1,2,3,4]` in effect)
    
    Returns
    -------
    pair of (int,float)
       First element of pair is the successor state as int in [0,mdp.stateMax] 
       (inclusive). Second element is the associated reward.
    """
    ### YOUR CODE HERE
    ### YOUR CODE HERE
    ### YOUR CODE HERE

    succlist = mdp.successors(s, a)
    p_list=[]
    for i in succlist:
        p_list.append(i[1])
    successor = random.choices(succlist, p_list)
    return successor[0][0], successor[0][2]



# OBLIGATORY FUNCTION:
# Qlearning returns the Q-value function after performing the given
#   number of iterations i.e. Q-value updates.
def Qlearning(mdp,gamma,lambd,iterations):
    """
    Perform the Q-learning algorithm on Markov Decision Process."

    Parameters
    ----------
    mdp : GridMDP object (see `qlearnexamples.py`)
       Markov Decision Process
    gamma : float in [0,1]
       Discount factor.
    lambd : float in [0,1]
       Learning rate.
    iterations : int > 0
       Number of iterations to perform.
    
    Returns
    -------
    dict {(state,action) : float}
       Q-values mapping from state (int in [0,mdp.stateMax] inclusive), action 
       (int in mdp.ACTIONS [s.t. the action is applicable in state)) pair to a the q-value.
    """

    # The Q-values are a real-valued dictionary Q[s,a] where s is a state and a is an action.
    state = 0 # Always start from state 0

    Q = dict()
    for s in range(mdp.stateMax+1):
        for a in mdp.applicableActions(s):
            Q[s,a]=0

    for i in range(iterations):
        a=random.choice(mdp.applicableActions(state))
        (succ,rew)=execute(mdp, state, a)
        max_Q=0
        for succ_a in mdp.applicableActions(succ):
            if Q[succ, succ_a]> max_Q:
                max_Q = Q[succ, succ_a]

        Q[state, a]=(1-lambd)*Q[state,a]+lambd*(rew+gamma*max_Q)
        state=succ

    ### YOUR CODE HERE
    ### YOUR CODE HERE
    ### YOUR CODE HERE

    return Q




# OBLIGATORY FUNCTION:
# makePolicy constructs a policy, i.e. a mapping from state to actions,
#   given a Q-value function as produced by Qlearning.
def makePolicy(mdp,Q):
    """
    Get policy for states in `mdp` given Q-values `Q`.

    Parameters
    ----------
    mdp : GridMDP object (see `qlearnexamples.py`)
       Markov Decision Process
    Q : dict {(state,action) : float}
       As returned by function `Qlearning`.

    Returns
    -------
    dict {state : action}
       Policy as a dict, mapping from every state of `mdp` 
       (int in [0,mdp.stateMax] inclusive) to the best choice of action 
       (int in mdp.ACTIONS) in that state.
    """
    # A policy is an action-valued dictionary P[s] where s is a state
    P = dict()

    for s in range(mdp.stateMax):
        max_Q=0
        for a in mdp.applicableActions(s):
            if Q[s,a] >= max_Q:
                max_Q=Q[s,a]
                P[s]=a

    ### YOUR CODE HERE
    ### YOUR CODE HERE
    ### YOUR CODE HERE
    return P




# OBLIGATORY FUNCTION:
# makeValues constructs the value function, i.e. a mapping from states to values,
#   given a Q-value function as produced by Qlearning.
# Note: It is expected that this function returns a dictionary with with keys
# for every state in mdp. However, it may be that your Q lacks values for some
# state/action combination. For these, you can use a dummy value of -1.
def makeValues(mdp,Q):
    """
    Get best values for states in `mdp` given Q-values `Q`.
    
    Parameters
    ----------
    mdp : GridMDP object (see `qlearnexamples.py`)
       Markov Decision Process
    Q : dict {(state,action) : float}
       As returned by function `Qlearning`.
    
    Returns
    -------
    dict {state : float}
       Values of best action in state for every state of `mdp` 
       (int in [0,mdp.stateMax] inclusive) to the Q-value of the
       best action in that state.
    """
    # A value function is a real-valued dictionary V[s] where s is a state
    V = dict()
    
    for s in range(mdp.stateMax):
        max_Q=0
        for a in mdp.applicableActions(s):
            if Q[s,a] >= max_Q:
                max_Q=Q[s,a]
                V[s]=max_Q
                
    ### YOUR CODE HERE
    ### YOUR CODE HERE
    ### YOUR CODE HERE
    return V
