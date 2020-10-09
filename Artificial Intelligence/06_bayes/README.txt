# =============================================
Python implementation for calculating probabilities and inference on bayes network

- You need numpy in order to run the code
    - On school computers you can use "module load anaconda3" to get required libraries for the session
    - Or, to install for your own computer, use "pip install numpy"

- Modify submission.py file according to the instructions TODO's.
- Submit the same file for both programming exercises on round 4

- To test your implementation locally run: python3/python2 test.py 

# =============================================
                Basic overview

You should complete tasks: 1.1, 1.2, 2.1, 2.2

Completing conditional probability and CPT parts enable you to construct bayes network

Feature - Index pairs are marked in data/mapping.py file 

Bayes network is defined as a class in network.py
    - Every node in the network has list of children and parents
    - Id of a node is given by it's index in the data that was observed
    - Every node has a conditional probability table with respect of it's parents
        - Table is implemented as dictionary where assignment to the parents responds to some probability value
        - To get a probability for a node, all of it's parents need some assignment

submission.py implements general implementations of what was used in the lecture 
    - You need to fill in the missing parts of the code

running test.py replicates the examples that were used in the lecture
    - Values should match of those seen in lecture
# =============================================