#remove 'listops.' from import. Only there for my Pythonista
from listops.listOperations import *
from collections import deque


class fAndS:
  '''
  state[0] is near side
  state[1] is far side

  state[n][0] is fox
  state[n][1] is sheep
  state[n][2] is 'boat on this side' (1 means on that side, 0 means not)
  '''


  def __init__(self, nf, ns, boatCapacity, state=None, history = []):
    '''
    nf = number of foxes
    ns = number of sheep
    '''
    self.nf = nf
    self.ns = ns
    self.bc = boatCapacity
    self.start = ((self.nf, self.ns, 1), (0, 0, 0))
    self.end = ((0, 0, 0), (self.nf, self.ns, 1))
    self.state = state or self.start[:]
    self.history = history or [self.state[:]]

  def isGoal(self):
    return self.state == self.end

  def isValid(self, st8):
    for side in st8:
      if side[0] > side[1] and side[1] != 0:
        return False
      if side[0] > self.nf or side[1] > self.ns:
        return False
      if side[0] < 0 or side[1] < 0:
        return False
    
    return st8 not in self.history

  def movement(self, change):
    curState = list(self.state[:])
    if curState[0][2]:
      curState[0] = tuple(
        funcLists(sub, curState[0], change)
        )
      curState[1] = tuple(
        funcLists(add, curState[1], change)
        )
    else:
      curState[0] = tuple(
        funcLists(add, curState[0], change)
        )
      curState[1] = tuple(
        funcLists(sub, curState[1], change)
        )
    return tuple(curState)

  def successors(self):
    possibleMoves = []
    for f in range(self.nf+1):
      for s in range(self.ns+1):
        if 0 < f+s <= self.bc:
          possibleMoves.append([f, s, 1])
          
    for move in possibleMoves:
      nextMove = self.movement(move)
      if self.isValid(nextMove):
        yield fAndS(self.nf, self.ns, self.bc, nextMove, self.history + [(nextMove)])


def process(numFox, numSheep, boatCapacity):
  '''Processes solutions'''
  state = fAndS(numFox, numSheep, boatCapacity)
  nextActions = deque()
  nextActions.append(state)
  previousActions = set()
  while nextActions:
    state = nextActions.popleft()
    if state.isGoal():
      yield state
    previousActions.add(state)
    children = state.successors()
    for child in children:
      if (child not in nextActions) or (child not in previousActions):
        nextActions.append(child)
  

class solutions:
  def __init__(self, nf, ns, bc):
    self.sols = tuple(process(nf, ns, bc))
  
  def stepForm(self, stepNum, step):
    '''Formats a step'''
    return 'Step {}: {}F {}S {}B | {}F {}S {}B'.format(stepNum, *step[0], *step[1])
    
  def solForm(self, solNum, sol):
    '''Formats a solution'''
    header = f'Solution {solNum}:\n{"-"*25}\n'
    body = '\n'.join([self.stepForm(stepNum, step) for stepNum, step in enumerate(sol)])
    tail = '\n' + '-'*25
    
    return header + body + tail
  
  def printout(self):
    '''Prints all solutions'''
    solList = self.sols
    print('Solutions')
    print('='*25)
    for sn, s in enumerate(solList, start=1):
      print(self.solForm(sn, s.history))
      
  def shortList(self):
    '''Prints the shortest solutions'''
    solList = self.sols
    smallLen = len(min(solList, key=lambda x: len(x.history)).history)
    print('='*25)
    print('Short solutions:')
    print('-'*25)
    
    smallList = []
    for sn, s in enumerate(solList, start=1):
      if len(s.history) == smallLen:
        print(self.solForm(sn, s.history))
        smallList.append([sn, s])
      else:
        break


