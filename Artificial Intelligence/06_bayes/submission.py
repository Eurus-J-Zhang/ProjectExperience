# Dont modify the imports, extra imports will be removed
import itertools
import numpy
from data.mapping import * 
from network import *

# Returns number of data-rows where the rows have value specified by features
def get_data_frequency(data, features):
    # Inputs: 
    #       - data : NxD list of recorded occurences
    #       - Features : dictionary of (data_index:value) pairs
    # Outputs: 
    #       - Number of corresponding samples
    return len([item for item in data if all(item[feature] == val for feature, val in features.items())])

# Get conditional probability for given query
def get_conditional_probability(data, query, condititions):
    # Inputs: 
    #       - data : NxD list of recorded occurences
    #       - query : Dictionary with (feature : val) pairs
    #       - condititions : 1xD dictionary of (B : val_B, ..., Z : val_Z) pairs 
    # Outputs: 
    #       - (float): Probability of P(A | B...Z) = P(A & B & ... & Z) / P(B & ... & Z)
    epsilon = 10e-5
    # Dictionary with query A and conditions B...Z
    combined_dictionary = query.copy()
    combined_dictionary.update(condititions)
    # =========================================================
    # TASK 1.1
    #  - Calculate P(A | B...Z)
    # TODO: student
    #  1. Return |data(query & conditions)| / (|data(conditions)| + epsilon)
    #  - you can use get_data_frequency(..) 
    
    # =========================================================
    #pass
    # =========================================================
    return get_data_frequency(data,combined_dictionary)/(get_data_frequency(data,condititions)+epsilon)

# Construct a CPT based on query and list of conditional variables
def construct_probability_table(data, query, conditions):
    # Go over possible assignments for condition-variables and calculate conditional probability for query variable
    # Inputs: 
    #       - data : NxD list of recorded occurences
    #       - query : Index that the query is based on
    #       - condititions : list of indexes we want to condition the search with
    # Outputs: 
    #       - Dictionary with (assignment : probability) pairs
    A = {query : 1}
    result = {}
    
    # List of all ways for assigning binary numbers to the conditions
    assignments = list(itertools.product([0, 1], repeat=len(conditions)))
    
    # Loop over all assignments of binary variables
    for assignment in assignments:
        # construct dictionary of (condition:assignment) pairs
        B = dict(zip(conditions, list(assignment)))
        # USE THIS KEY TO STORE RESULTS TO DICTIONARY
        dict_key = "vals"
        dict_key += "".join([".{}:{}.".format(key, B[key]) for key in sorted(B.keys())])
        # =========================================================
        # TASK 1.2
        #  - Construct a dictionary where 
        #       - keys are assignments of condition variables (key is provided) 
        #       - values are the conditional probabilities P(query|key)
        # 
        # TODO: student
        
        result[dict_key]=get_conditional_probability(data, A, B)
        
        
        #  1. Calculate the conditional probability for the current assignment of variables: B
        #     - You can use get_conditional_probability(...)
        #  2. Store the probability to result dictionary with key: dict_key
        # =========================================================
        #pass
        # =========================================================
    return result

# Evaluate probability P(query = val | conditions)
def evaluate_node(G, query, val, conditions):
    # Inputs: 
    #       - G          : Bayesian network
    #       - query      : node_id of the query variable 
    #       - val        : value that node_id should have
    #       - conditions : dictionary of (node_id:val) pairs
    return G.get_node_probability(query, conditions) if val == 1 else 1 - G.get_node_probability(query, conditions)

# Get all variables of G in topological order
def get_topological_order(G):
    # Use BFS to find the order of variables in the network
    queue = G.roots[:]
    visited = set()
    for root in queue:
        visited.add(root.data_id)
    X = []
    while queue:
        node = queue.pop(0)
        X.append(node.data_id)
        for new_node in node.children:
            if new_node.data_id not in visited and all(n in visited for n in new_node.parents):
                visited.add(new_node.data_id)
                queue.append(new_node)
    return X

# Calculate probability distribution by brute force exhaustive enumerating
def exhaustive_enum(G, X, E, e):
    # Inputs: 
    #       - G : Bayesian network
    #       - X : Ordered list of all terms in G
    #       - E : Terms that are fixed
    #       - e : values for the fixed terms
    # Outputs: 
    #       - (float): probability P(X | e)
    total = 0
    fixed_dictionary = dict(zip(E, e))
    # Make all assignments for non-fixed terms
    free_variables = [val for val in X if val not in E]
    assignments = list(itertools.product([0, 1], repeat=len(free_variables)))

    # Go over the assignments and calculate network product for each of them
    # Look for: Exhaustive Enumeration in chapter 4.4
    for assignment in assignments:
        # Create a combined dictionary of assignment to free variables and fixed variables
        free_dictionary = dict(zip(free_variables, list(assignment)))
        combined_dictionary = fixed_dictionary.copy()
        combined_dictionary.update(free_dictionary)
 
        tmp = 1
        # Calculate product of probabilities in G given the assignment
        for node in G.nodes:
            
            
            # =========================================================
            # TASK 2.1: From exhaustive search in chapter 4.4
            #  - Calculate product for all probabilities over all of the nodes 
            # TODO: student
            #  1. Calculate probability P(node | parents(node)) and accumulate a product over nodes
            #    - You can use evaluate_node(...) 
            #       - If you pass all current conditions to the method, the exess ones are cut out 
            #  2. accumulate the sum once final product is calculated
            #  3. Return the complete sum
            
            val=combined_dictionary[node.data_id]
            
            probability_node=evaluate_node(G, node.data_id, val, combined_dictionary)
            
            tmp=tmp*probability_node
            # 
            #  HINTS: 
            #   - See exhaustive search in chapter 4.4
            #   - combined dictionary consists of (node:binary) assignments
            # =========================================================
            #break
            # =========================================================
        total +=tmp
    return total

# Calculate distribution P(targets | e) by brute force search over the hidden variables y
def brute_force(G, targets, E, e):
    # Inputs: 
    #       - G         : Bayesian network
    #       - targets   : A list of variables that we want to calculate distribution over
    #       - E         : Data-indexes of terms that are fixed
    #       - e         : values for the fixed terms
    # Outputs: 
    #       - probability P(targets | e)

    # Get all variables of G
    X = get_topological_order(G)
    # Calculate probabilities over the possible assignments to target variables
    # one where targets are assigned to 1 and one when targets are assigned to 0
    pos = exhaustive_enum(G, X, E + targets, e + [1 for _ in range(len(targets))])
    neg = exhaustive_enum(G, X, E + targets, e + [0 for _ in range(len(targets))])
    # Return a normalized probability
    return pos / (pos + neg + + 1e-10)


# Generates random assignment of X based on E
def sample(G, X, E, e):
    # Inputs: 
    #       - G : Bayesian network
    #       - X : Ordered list of all terms
    #       - E : Fixed features of the sample
    #       - e : Values of the fixed features
    # Outputs: 
    #       - (list)(float): Assigment for each variable in X and corresponding weight: w
    variables = []
    assignment = []
    w = 1
    
    # Algorithm Sample(..) in chapter 4.4
    for variable in X:
        parents = dict(zip(variables, assignment))
            # =========================================================
            # TASK 2.2: complete the algorithm as in algorithm SAMPLE(..) on chapter 4.4
            #
            # TODO: student
            #  1. If variable: var is in list E
            #     - assign: var = e[var]
            #     - update: w = w * P(var = e[var] | parents(var))
            #     
            #  2. If variable: var is not in list E
            #     - calculate prob = P(var = True | parents(var))
            #     - Generate: y = random([0, 1))
            #     - if y < prob assign var to 1, else assign var to 0
            #
            #  3. always store varables and assignments
            #
            #  - Use G.get_node_probability(query, parents) to get P(query | parents(query))
            #    - Inputs: query = variable id, parents = dictionary of (parent_id : 0|1 )
            #    - You can pass all current assignments as parents(query) and bayes network will ignore irrelevant variables
            # =========================================================
        if variable in E:
            # Get the fixed value for variable in e
            index = numpy.where(numpy.array(E) == variable)[0][0]
            value = e[index]
            
            w=w*evaluate_node(G, variable, value, parents)

            
            variables.append(variable)
            assignment.append(value)
            
            # =========================================================
            #pass
            # =========================================================
        else:
            
            prob=G.get_node_probability(variable, parents)
            y=numpy.random.random(1)[0]
            
            if y<prob:
                value=1
            else:
                value=0
            
            variables.append(variable)
            assignment.append(value)
            
            
            # =========================================================
            #pass
            # =========================================================
    return assignment, w

# Approximate a joint distribution of targets
def approximate_distribution(G, targets, E, e):
    # Inputs: 
    #       - G         : Bayesian network
    #       - targets   : A list of variables that we want to calculate distribution over
    #       - E         : Fixed features of the sample
    #       - e         : Values of the fixed features
    # Outputs: 
    #       - Approximated probability P(targets|e)

    N = 2000
    pos_weight = 0
    total_weight = 0
    X = get_topological_order(G)

    # Make mapping of targets to X for checking when all target variables are true
    query_mapping = [X.index(target) for target in targets]

    for _ in range(N):
        tmp, w = sample(G, X, E, e)
        # Accumulate the sum only when all variables in distribution are true
        if len(tmp) > 0 and all(tmp[mapping] == 1 for mapping in query_mapping):
            pos_weight += w
        total_weight += w
    return pos_weight/(total_weight+1e-10)
