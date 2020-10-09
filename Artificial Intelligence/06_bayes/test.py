from network import *
from submission import *
from data.mapping import * 

import numpy as np
import re

# Construct bayesian network 
def construct_sample_network(data):
    network = bayes_network(data)
    # You need to list the nodes so that parents are introduced before children
    # You can inspect data.mapping to see all the features
    network.append_node(MEDICALSERV, "MEDICALSERV", [])
    network.append_node(SCHOOLHYMN, "SCHOOLHYMN", [MEDICALSERV])
    network.append_node(MILSERVICE, "MILSERVICE", [MEDICALSERV])
    network.append_node(METROPOLIS, "METROPOLIS", [SCHOOLHYMN])
    network.append_node(NATO, "NATO", [MILSERVICE])
    network.append_node(SAIMAASEAL, "SAIMAASEAL", [SCHOOLHYMN, MILSERVICE])
    return network


def is_answer_close(a, b, EPSILON = 1e-2):
    return abs(a - b) <= EPSILON

# See that constructed CPT matches the example
def task_conditional_probability(data):
    tests = [({SAIMAASEAL : 1}, {MILSERVICE : 1, SCHOOLHYMN: 1}, ["SAIMAASEAL", "MILSERVICE", "SCHOOLHYMN"], 0.857),
        ({NATO : 1}, {MILSERVICE : 0}, ["NATO", "-MILSERVICE"], 0.82),
        ({MEDICALSERV : 1}, {}, ["MEDICALSERV"], 0.128),
        ({SAIMAASEAL : 1}, {MILSERVICE : 0, SCHOOLHYMN: 1}, ["SAIMAASEAL", "-MILSERVICE", "SCHOOLHYMN"], 0.790)]

    for query, conditions, fields, answer in tests:
        prob = get_conditional_probability(data, query, conditions)
        if is_answer_close(prob, answer):
            print("correct probability P({}|{}) = {}".format(fields[0], " & ".join(fields[1:]), round(prob,3)))
        else:
            print("Conditional probability failed: got {}, true answer {}".format(prob, answer))

# See that constructed CPT matches the example
def task_cpt(data):
    tests = [(SAIMAASEAL, [MILSERVICE, SCHOOLHYMN], ["SAIMAASEAL", "MILSERVICE", "SCHOOLHYMN"], {"0 0":0.587, "0 1":0.790, "1 0":0.834, "1 1":0.857}),]

    for query, conditions, fields, answer in tests:
        table = construct_probability_table(data, query, conditions)

        print("Calculating CPT for P({}|{})".format(fields[0], " & ".join(fields[1:])))
        print("{} : {}".format(" ".join(fields[1:]), fields[0]))
        for key, probability in table.items():
            assignments = re.findall(".([0-9]+):([0-1]).", key)
            str_assignment = " ".join([val for _, val in assignments])
            passed = "Correct" if is_answer_close(answer[str_assignment], probability) else "Not right probability, correct: {}".format(answer[str_assignment])
            print("{} : {} <- {}".format(str_assignment, round(probability, 3), passed))

def test_brute_force(data, network):
    tests = [([MILSERVICE], ([MEDICALSERV, SAIMAASEAL, METROPOLIS], [0, 0, 0]), ["MILSERVICE", "MEDICALSERV", "SAIMAASEAL", "METROPOLIS"], 0.183)]

    for query, (E,e), fields, answer in tests:
        prob = brute_force(network, query, E, e)

        print("Calculating P({}|{})".format(fields[0], " & ".join(fields[1:])))
        if is_answer_close(answer, prob):
            print("Correct probability {}".format(round(prob, 3)))
        else:
            print("Wrong, true answer was {} while yours was {}".format(answer, round(prob, 3)))

def test_sampling(data, network):
    tests = [([MILSERVICE], ([MEDICALSERV, SAIMAASEAL, METROPOLIS],  [0, 0, 0]), ["MILSERVICE", "MEDICALSERV", "SAIMAASEAL", "METROPOLIS"], 0.183)]

    for query, (E,e), fields, answer in tests:
        prob = [approximate_distribution(network, query, E, e) for _ in range(3)]
        print("Calculating P({}|{})".format(fields[0], " & ".join(fields[1:])))

        if any([is_answer_close(answer, p, EPSILON = 3e-2) for p in prob]):
            print("Correct probability {}".format(round(np.average(prob), 3)))
        else:
            print("Wrong, true answer was {} while yours was {}".format(answer, round(np.average(prob), 3)))

def main():
    # Load data
    filename = "data/hs.txt"
    data = np.loadtxt(filename, delimiter=" ")
    
    # Construct same bayesian network as in the lecture
    network = construct_sample_network(data)

    print("\n===\nTesting conditional probability\n===")
    task_conditional_probability(data)

    print("\n===\n Making CPT\n===")
    task_cpt(data)

    print("\n===\nTesting brute force inference\n===")
    test_brute_force(data, network)

    print("\n===\nTesting sampling\n===")
    test_sampling(data, network)


if __name__ == "__main__":  
    main()