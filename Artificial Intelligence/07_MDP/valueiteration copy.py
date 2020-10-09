"""
This module contains functions used to perform the value iteration algorithm
on markov descision processes implemented using the class mdp.MDP (see mdp.py)

The function `value_iteration` performs the value iteration steps on a 
descision process until the sensitivity condition given by epsilon is met
and returns a dictionary from states to values.

The function `make_policy` returns a policy (a dictionary from states to actions)
given a process, and set of values (as computed by the value_iteration function).

The function `value_of` is a helper function calculating the sum over all successor
states given a process, and a start state and action of this process.
Used in both `value_iteration` and `make_policy`.

The function `argmax` is a helper function, giving the key with maximum value for a 
dictionary.

The parameter `mdp` is an instance of a class deriving from mdp.MDP.

The parameter `gamma` is always the discount factor and a float value.

"""

def value_of(mdp, s, a, v, gamma):
    
    """
    Compute the value of taking action `a` in state `s` in `mdp` with respect existing values in `v`.

    Should, given state $s$, action $a$, and discount factor $\gamma$ compute 
    $\sum_{s' \in S} P(s,a,s') * ( R(s,a,s') + \gamma * v(s') )$
    where $S$ is the set of successor states to $s$ and $a$.

    Parameters
    ----------
    mdp : mdp.MDP
    s : state
    a : action
    v  : dict of state : float
       value of states at time t - 1
    gamma : float in ]0,1[

    Returns
    -------
    float
       New value.
    """

    ss=mdp.successor_states(s, a)
    vv=0
    for s2 in ss:
        vv+= mdp.P(s,a,s2)*(mdp.R(s,a,s2)+gamma*v[s2])
        
    return vv

    pass  

    

    # -------- TASK 2.1 --------------------------------------------------------
    # TASK: Implement the function computing the sum described above and return
    # the value as a float. Look at the documentation for mdp.MDP to see how
    # the rewards R and probabilities P can be retrieved.
    #
    # CODE HERE CODE HERE CODE HERE
    
        
def value_iteration(mdp, gamma, epsilon = 0.001):
    """
    Perform value iteration of Markov Descision Process MDP.
    
    Parameters
    ----------
    mpd : mdp.MPD object
       Markov Descision Process
    gamma : float > 0
       Discount factor
    epsilon : float > 0
       Algorithm sensitivity.
    
    Returns
    -------
    dict of state : float
       Map from state to value, where state is in mdp.states.
    """
    # -------- TASK 2.2 --------------------------------------------------------
    # TASK: Implement the value iteration algorithm
    # This corresponds to step 1 - 3 of the algorithm as described on the
    # MyCourses pages
    # The return value, v, should be a dictionary mapping from states
    # to values. This corresponds to v_{n+1} once the change is small
    # enough in step 3 and the algorithm terminates.
    #
    # CODE HERE CODE HERE CODE HERE
    #
    
    states=mdp.states()
    
    v=[{}]
    

    for s in states:
        v[0][s]=0   
         
    
    for n in range(0,10000):
        v.append({})

        
        for s in states:
            v_candidate=[]
            for a in mdp.applicable_actions(s): 
                for s2 in mdp.successor_states(s,a):
                    v_candidate.append(value_of(mdp, s, a, v[n], gamma))

            v[n+1][s]=max(v_candidate)
        

        validation_value=0

        if n == 0:
            continue
        for s in states:

            if abs(v[n][s]-v[n-1][s])< epsilon*(1-gamma)/(2*gamma):
                validation_value+=0
            else:
                validation_value+=1
        if validation_value==0:
            break

            
    return v[n]
            
    
    
    
    
    pass
    
def argmax(d):
    """
    Return key corresponding to maximum value in dictionary `d`.

    If several keys have the same maxum value, one of them will be returned.

    Parameters
    ----------
    d : dict
       values must be numeric
    
    Returns
    -------
    key in `d`
    """
    return max(d, key = lambda k : d[k])

def make_policy(mdp, optimal_values, gamma):
    """
    Compute policy given optimal values for all states.

    Parameters
    ----------
    TODO

    Returns
    -------
    dict of state : action
       Where state in mdp.states().
    """
    return {s1 : argmax({a : value_of(mdp, s1,a, optimal_values, gamma)
                         for a in mdp.applicable_actions(s1)})
            for s1 in mdp.states()}

if __name__ == "__main__":
    # Very basic examples.
    #
    # For more and tests with automatic compariason run test_valueiteration.py

    from gridmdp import GridMDP
    
    print("--- Example 1 ------------------")
    # A grid with two walls (#), one positive reward (+)
    # and one negative (-). (.) denotes neutral (0.0).
    gdp = GridMDP([".+.",
                   "-.#",
                   "#.."])

    print("Input GridMDP:")
    print(gdp)

    gamma = 0.8
    epsilon = 0.01
    v = value_iteration(gdp, gamma, epsilon)
    pi = make_policy(gdp,v,gamma)

    print("Computed values and policy")
    for s in sorted(gdp.states()):
        print("Location: {0} \t | Value: {1} \t | Policy: {2}".format(s, v[s], pi[s]))
    print(
"""
CORRECT VALUES (Policy may differ if multiple actions has the same value)
Location: (0, 0)         | Value: 2.166637350797169      | Policy: East
Location: (0, 1)         | Value: 1.8238205241911116     | Policy: East
Location: (0, 2)         | Value: 2.29341219866735       | Policy: West
Location: (1, 0)         | Value: 1.5860931388905264     | Policy: North
Location: (1, 1)         | Value: 2.1666373507971692     | Policy: North
Location: (2, 1)         | Value: 2.29341219866735       | Policy: South
Location: (2, 2)         | Value: 1.7940038893976213     | Policy: South
""")
    print("--- Example 2 ------------------")
    gdp = GridMDP(["...+",
                   ".#.-",
                   "...."])
    print("Input GridMDP:")
    print(gdp)
    gamma = 0.8
    epsilon = 0.01
    v = value_iteration(gdp, gamma, epsilon)
    pi = make_policy(gdp,v,gamma)
    print("Computed values and policy")
    for s in sorted(gdp.states()):
        print("Location: {0} \t | Value: {1} \t | Policy: {2}".format(s, v[s], pi[s]))
    print(
"""
CORRECT VALUES (Policy may differ if multiple actions has the same value)
Location: (0, 0)         | Value: 2.1870595721840265     | Policy: West
Location: (0, 1)         | Value: 1.6360669646671202     | Policy: East
Location: (0, 2)         | Value: 2.1870595721840265     | Policy: East
Location: (0, 3)         | Value: 1.7541002681521682     | Policy: North
Location: (1, 0)         | Value: 1.601186507019843      | Policy: North
Location: (1, 2)         | Value: 1.601186507019843      | Policy: North
Location: (1, 3)         | Value: 2.1785706078376768     | Policy: North
Location: (2, 0)         | Value: 1.7072985613492146     | Policy: West
Location: (2, 1)         | Value: 1.329565025014288      | Policy: East
Location: (2, 2)         | Value: 1.7072985613492149     | Policy: East
Location: (2, 3)         | Value: 2.195548536530376      | Policy: South
""")
    
    print("--- Example 3 ------------------")
    print("Example using a basic two-state machine.")
    
    from twostatemachine import TwoStateMachine
    tsm = TwoStateMachine()
    gamma = 0.5
    epsilon = 0.01
    vi = value_iteration(tsm, gamma, epsilon)
    va = tsm.analytic(gamma)
    print("""(using gamma = {0}, epsilon = {1})

Iterated values 
---------------
upright: {2}
prone  : {3}

Theoretical values
------------------
upright: {4}
prone  : {5}

""".format(gamma,epsilon,
           vi[TwoStateMachine.States.upright],
           vi[TwoStateMachine.States.prone],
           va[TwoStateMachine.States.upright],
           va[TwoStateMachine.States.prone]
           ))
    



