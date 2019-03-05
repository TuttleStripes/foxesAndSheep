from listOperations import *


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

    self.posMoves = set()
    for f in range(self.nf+1):
      for s in range(self.ns+1):
        if 0 < f+s <= self.bc:
          self.posMoves.add((f, s, 1))


  def isGoal(self, st8):
    return st8 == self.end

  def isValid(self, st8):
    for side in st8:
      if side[0] > side[1] and side[1] != 0:
        return False
      if side[0] > self.nf or side[1] > self.ns:
        return False
      if side[0] < 0 or side[1] < 0:
        return False
    
    return True

  def movement(self, st8, change):
    curState = list(st8[:])
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

  def successors(self, st8=None):
    st8 = st8 or self.state[:]
    for move in self.posMoves:
      nextMove = self.movement(st8, move)
      if self.isValid(nextMove):
        yield [st8, nextMove]



def process(nf, ns, bc):
  main = fAndS(nf, ns, bc)
  history = list(main.successors())
  while history:
    curHis = history.pop()
    curState = curHis[-1]
    if main.isGoal(curState):
      yield curHis
    children = main.successors(curState)
    for child in children:
      if child[-1] not in curHis:
        history.append(curHis+[child[-1]])



class solutions:
  def __init__(self, nf, ns, bc):
    self.params = (nf, ns, bc)
    self.solList = process(*self.params)
  
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
    solList = process(*self.params)
    print('Solutions')
    print('='*25)
    for sn, s in enumerate(solList, start=1):
      print(self.solForm(sn, s))
      
  def shortest(self, acceptable=None):
    '''Prints the shortest solutions'''
    sols = process(*self.params)
    short = (1, next(sols))
    for i, v in enumerate(sols, start=2):
      if len(v) < len(short[1]):
        short = (i, v)
      if acceptable:
        if len(v) <= acceptable:
          break 
    
    print('Shortest solution')
    print('=' * 25)
    print(self.solForm(*short))


if __name__ == '__main__':
  nf = int(input('Number of foxes: '))
  ns = int(input('Number of sheep: '))
  bc = int(input('Boat capacity: '))
  sols = solutions(nf, ns, bc)
  
  
