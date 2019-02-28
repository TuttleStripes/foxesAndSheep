from listOperations import *


class fAndS:
  '''
  state[0] is near side
  state[1] is far side

  state[n][0] is fox
  state[n][1] is sheep
  state[n][2] is 'boat on this side' (1 means on that side, 0 means not)
  '''
  start = [[3, 3, 1], [0, 0, 0]]
  end = [[0, 0, 0], [3, 3, 1]]


  def __init__(self, nf, ns, boatCapacity, state=None, history = []):
    self.nf = nf
    self.ns = ns
    self.bc = boatCapacity
    self.start = [[self.nf, self.ns, 1], [0, 0, 0]]
    self.end = [[0, 0, 0], [self.nf, self.ns, 1]]
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
    curState = self.state[:]
    if curState[0][2]:
      curState[0] = list(
        funcLists(sub, curState[0], change)
        )
      curState[1] = list(
        funcLists(add, curState[1], change)
        )
    else:
      curState[0] = list(
        funcLists(add, curState[0], change)
        )
      curState[1] = list(
        funcLists(sub, curState[1], change)
        )
    return curState

  def successors(self):
    possibleMoves = []
    for f in range(self.nf+1):
      for s in range(self.ns+1):
        if 0 < f+s <= self.bc:
          possibleMoves.append([f, s, 1])
          
    for move in possibleMoves:
      nextMove = self.movement(move)
      if self.isValid(nextMove):
        yield fAndS(self.nf, self.ns, self.bc, nextMove, self.history + [nextMove])


def process(numFox, numSheep, boatCapacity):
  state = fAndS(numFox, numSheep, boatCapacity)
  nextActions = [state]
  previousActions = []
  while nextActions:
    state = nextActions.pop(0)
    if state.isGoal():
      yield state
    previousActions.append(state)
    children = state.successors()
    for child in children:
      if (child not in nextActions) or (child not in previousActions):
        nextActions.append(child)
  


class solutions:
  def __init__(self, nf, ns, bc):
    self.sols = list(process(nf, ns, bc))
  
  def stepForm(self, stepNum, step):
    return 'Step {}: {}F {}S {}B | {}F {}S {}B'.format(stepNum, *step[0], *step[1])
    
  def solForm(self, solNum, sol):
    header = f'Solution {solNum}:\n{"-"*25}\n'
    body = '\n'.join([self.stepForm(stepNum, step) for stepNum, step in enumerate(sol)])
    tail = '\n' + '-'*25
    
    return header + body + tail
  
  def printout(self):
    print('Solutions')
    print('='*25)
    for sn, s in enumerate(self.sols, start=1):
      print(self.solForm(sn, s.history))
      
  def smallest(self):
    smallLen = len(min(self.sols, key=lambda x: len(x.history)).history)
    print('='*25)
    print('Smallest solutions:')
    for sn, s in enumerate(self.sols, start=1):
      if len(s.history) == smallLen:
        print(self.solForm(sn, s.history))
    


if __name__ == '__main__':
  solutes = solutions(5,5,3)
