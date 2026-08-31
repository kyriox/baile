import sys
import os
import numpy as np

baile_path = os.path.abspath(os.path.join(".", "src"))
test_path = os.path.abspath(os.path.join(".", "test"))
if not baile_path in sys.path:
    sys.path.append(baile_path)
if not test_path in sys.path:
    sys.path.append(test_path)
import SimpleSearch as ss

# Initial state of the board. Later a spot will be removed.
tablero = [[1],
           [1, 1],
           [1, 1, 1],
           [1, 1, 1, 1],
           [1, 1, 1, 1, 1]]

# pegsRestantes = 15


def remove(i, j, tablero, x=0, y=0, withJump=False):
    """ 
    Returns new board configuration.
    i,j are the current position in board
    x and y are the increments around the current position
    withJump is only used when solving the board, 
    at first is not used and it only removes one spot
    """
    newTablero = tablero
    if withJump:
        # old spot is replaced with 0
        newTablero[i][j] = 0
        # jumped peg is replaced with 0
        newTablero[i+x][j+y] = 0
        # landing spot
        newTablero[i+2*x][j+2*y] = 1
        # pegsRestantes = pegsRestantes - 1
        # print(pegsRestantes)
        return newTablero
    newTablero[i][j] = 0
    # pegsRestantes -1
    return newTablero


def jump(i, j, tablero, x, y):

    # next if statement checks that the current possition has a 1, that target peg is also 1, and the landing spot is empty
    try:
        if tablero[i][j] == 1 and tablero[i+x][j+y] == 1 and tablero[i+2*x][j+2*y] == 0:
            return remove(i, j, tablero, x, y, withJump=True)
    except IndexError:
        pass


def successorPeg(a):
    tablero = a.state  # current state
    successors = []
    # Possible movements ⬅️,➡️,⬇️,⬆️,↖️,↘️
    left, right = (0, 1, "left ⬅️"), (0, +1, "right ➡️")
    up, down = (1, 0, "down ⬇️"), (-1, 0, "up ⬆️")
    leftUp, rightDown = (-1, -1, "lefttUp ↖️"), (1, 1, "rightDown ↘️ ")

    #
    for i in range(5):
        for j in range(len(tablero[i])):
            for x, y, op in [up, down, left, right, leftUp, rightDown]:
                # all moves per position in the cell

                # print(f'X: {x} Y:{y}, op: {op} {tablero[i][j]}')
                # convert from tuple to list
                nboard = [list(bx[:]) for bx in tablero]
                # print(nboard[i])
                # function returns new board configuration
                nboard = jump(i, j, nboard, x, y)
                if nboard is not None:  # avoid None objects
                    # list-> tuple to make it hashable
                    nboard = tuple([tuple(row) for row in nboard])
                    # print(f"debug nboard{nboard}")
                    successors.append(ss.node(nboard, op=op,
                                              depth=a.depth+1, parent=a))
    return successors  # list of successors


def pegGoal(*states):
    """returns True if current node equals the goal"""
    if states[0] is None:
        print("error en el primero")
    if states[1] is not None:
        a = states[0]  # start state is the firts argument
        b = states[1]  # final state is the second...
        return a.state == b.state


# Board's target goal
tableroGoal = [[1],
               [0, 0],
               [0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0, 0]]

tableroinicio = remove(0, 0, tablero)
tableroinicio = tuple([tuple(row) for row in tableroinicio])
tableroGoal = tuple([tuple(row) for row in tableroGoal])

start = ss.node(tableroinicio, op="start")
final = ss.node(tableroGoal, op="final")

# successorPeg(start)

print("start's state: ", start.state)
print("start's parent: ", start.parent)
print("start's depth: ", start.depth)
print("final state: ", final.state)


# setting up
bfs = ss.BlindSearch(start, successorPeg, pegGoal,
                     goal_state=final, strategy="bfs")
# start search and print the amount to specific solutions to board.
resb = bfs.find()
print(resb.state)

print(resb.getPath())
