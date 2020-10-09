
from qlearn import *
from qlearnexamples import *

# Small test grid with teleports

testgrid1 = GridMDP(4,3,[0, 0, 0, 1,
                         0,99, 0,-1,
                         0, 0, 0, 0],
                    True)
testgrid1.show()

testgrid2 = GridMDP(7,5,[0,  0,  0,  0,  0,  0,  0,
                         0,  0,  0,  0,  0,  0,  0,
                         0,  0, -1,  2, -9,  0,  0,
                         0,  0,  0,  0,  0,  0,  0,
                         0,  0,  0,  0,  0,  0,  0],
                    False)

testgrid2.show()

testgrid3 = GridMDP(8,6,[0,  0,  0,  0,  0,  0,  0,  0,
                         0,  0,  0,  0,  0,  0,  0,  0,
                         0,  0, -9,  1,  1, -9,  0,  0,
                         0,  0, -9,  1,  1, -9,  0,  0,
                         0,  0,  0,  0,  0,  0,  0,  0,
                         0,  0,  0,  0,  0,  0,  0,  0],
                    False)

testgrid3.show()

Q1 = Qlearning(testgrid1,0.95,0.2,200000)
Q2 = Qlearning(testgrid2,0.95,0.2,200000)
Q3 = Qlearning(testgrid3,0.95,0.2,200000)

P1 = makePolicy(testgrid1,Q1)
P2 = makePolicy(testgrid2,Q2)
P3 = makePolicy(testgrid3,Q3)

V1 = makeValues(testgrid1,Q1)
V2 = makeValues(testgrid2,Q2)
V3 = makeValues(testgrid3,Q3)

testgrid1.showPolicy(P1)
testgrid2.showPolicy(P2)
testgrid3.showPolicy(P3)

testgrid1.showValues(V1)
testgrid2.showValues(V2)
testgrid3.showValues(V3)
