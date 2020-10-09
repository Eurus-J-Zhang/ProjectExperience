
Exercise: Markov Decision Processes and Value Iteration
--------------------------------------------------------

In this exercise you will implement a very simple Markov Chain, as well as
the value iteration algorithm for Markov Decision Processes.

The value iteration algorithm can then be applied to a little bit more advanced
grid decision process, where different locations on a 2D grid can have
varying rewards, and one wants to compute the value of each location, and the
corresponding policy.

1. To prepare for the exercise, make sure you have consulted the lecture slides
and MyCourses material related to Markov Processes, The Bellman Equation, and
Value Iteration.

2. You can also have a look at doc/TwoStateMachine.pdf for an example of Markov
chain process.

3. Look at the source code.
   - mdp.py :: This file defines an abstract class providing a general interface
     for Markov Decision Processes. No need to edit.
   - template-twostatemachine.py :: This defines a class implementing the simple
     machine described in doc/TwoStateMachine.pdf by inheriting from mdp.py
     TASKs 1.x are found here. Copy to twostatemachine.py
   - template-valueiteration.py :: Declares function related to value iteration
     TASKs 2.x are found here. Copy to valueiteration.py.
   - gridmdp.py :: This file defines a grid Markov Decision Process by
     inheriting from mdp.py. No need to edit.
   - gridactions.py :: Defines actions used by gridmdp.py. No need to edit.
   - test_twostatemachine.py :: Automated tests for twostatemachine.py
   - test_valueiteration.py :: Automated tests for valueiteration.py

3. TASK 1 - Implement some functionality on twostatemachine.py
   - Copy template-twostatemachine.py to twostatemachine.py
   - Read about the process in doc/TwoStateMachine.pdf
   - Look for instructions on TASK 1.1, 1.2, and 1.3 in twostatemachine.py

twostatemachine.py contains a basic example of its use which is executed by
`python twostatemachine.py`, however more explicit tests can be performed by
running `python test_twostatemachine.py` which contains a few unit tests.

4. TASK 2 - Implement Value Iteration
   - Copy template-valueiteration.py to valueiteration.py
   - Make sure to check the Value Iteration Algorithm in the MyCourses material
   - Look in mdp.py to find out the interface to get P, R, states, and
     applicable actions for a process.
   - Look for instructions on TASK 2.1, and 2.2 in the source code.

valueiteration.py contains a basic example of its use which is executed by
`python valueiteration.py`, however more explicit tests can be performed by
running `python test_valueiteration.py` which contains a few unit tests.

Good luck.

Note: The output from the test_*.py files will print errors at the top, and
fails below. If you get an error it may be due to one or more failures
listed below it. Try to address the fails in order, and they may also fix
the errors.
