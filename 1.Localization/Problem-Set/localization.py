'''
The function localize takes the following arguments:

colors:
       2D list, each entry either 'R' (for red cell) or 'G' (for green cell)

measurements:
       list of measurements taken by the robot, each entry either 'R' or 'G'

motions:
       list of actions taken by the robot, each entry of the form [dy,dx],
       where dx refers to the change in the x-direction (positive meaning
       movement to the right) and dy refers to the change in the y-direction
       (positive meaning movement downward)
       NOTE: the *first* coordinate is change in y; the *second* coordinate is
             change in x

sensor_right:
       float between 0 and 1, giving the probability that any given
       measurement is correct; the probability that the measurement is
       incorrect is 1-sensor_right

p_move:
       float between 0 and 1, giving the probability that any given movement
       command takes place; the probability that the movement command fails
       (and the robot remains still) is 1-p_move; the robot will NOT overshoot
       its destination in this exercise

The function should RETURN (not just show or print) a 2D list (of the same
dimensions as colors) that gives the probabilities that the robot occupies
each cell in the world.

Compute the probabilities by assuming the robot initially has a uniform
probability of being in any cell.

Also assume that at each step, the robot:
1) first makes a movement,
2) then takes a measurement.

Motion:
 [0,0] - stay
 [0,1] - right
 [0,-1] - left
 [1,0] - down
 [-1,0] - up
'''

def localize(colors,measurements,motions,sensor_right,p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]
    
    for i in range(len(measurements)):
        p = move(p, motions[i], p_move, colors)
        p = sense(p, measurements[i], sensor_right, colors)
    return p

def sense(p, Z, pHit, colors):
    pMiss = 1. - pHit
    q = [[0 for row in range(len(colors[0]))] for col in range(len(colors))]
    for x in range(len(p[0])):
        for y in range(len(p)):
            hit = (Z == colors[y][x]) 
            q[y][x] = (p[y][x] * (hit * pHit + (1-hit) * pMiss))
    s = sum(map(sum,q))
    for x in range(len(q[0])):
        for y in range(len(q)):
            q[y][x] = q[y][x] / s
    return q

def move(p, U, p_move, colors):
    p_stay = 1. - p_move
    q = [[0 for row in range(len(colors[0]))] for col in range(len(colors))]
    for x in range(len(q[0])):
        for y in range(len(q)):
            s = p_move * p[(y-U[0]) % len(p)][(x-U[1]) % len(p[0])]
            s += p_stay * p[y][x]
            q[y][x] = s
    return q

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print('[' + ',\n '.join(rows) + ']')