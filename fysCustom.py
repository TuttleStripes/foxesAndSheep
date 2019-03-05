from listops.listOperations import *
import time


class fAndS:
  '''
  state[0] is near side
  state[1] is far side

  state[n][0] is fox
  state[n][1] is sheep
  state[n][2] is 'boat on this side' (1 means on that side, 0 means not)
  '''

  def __init__(self, nf, ns, bc, state=None, history = []):
    '''
    nf = number of foxes
    ns = number of sheep
    bc = boat capacity
    '''
    self.nf = nf
    self.ns = ns
    self.bc = bc
    self.start = ((self.nf, self.ns, 1), (0, 0, 0))
    self.end = ((0, 0, 0), (self.nf, self.ns, 1))
    self.state = state or self.start[:]

    self.posMoves = set()
    for f in range(self.nf+1):
      for s in range(self.ns+1):
        if 0 < f+s <= self.bc:
          self.posMoves.add((f, s, 1))

  def isGoal(self, st8):
    '''Is the given state the end state?'''
    return st8 == self.end

  def isValid(self, st8):
    '''
    Returns False if the given state:
    * has more wolves than sheep on either side (if the side has a non-zero number of sheep)
    * more wolves/sheep than the original number of wolves/sheep
    * number of wolves/sheep is less than 0
    Otherwise returns True
    '''
    for side in st8:
      if side[0] > side[1] and side[1] != 0:
        return False
      if side[0] > self.nf or side[1] > self.ns:
        return False
      if side[0] < 0 or side[1] < 0:
        return False
    
    return True

  def movement(self, st8, change):
    '''Takes the current state and returns a modification of it based on the inputted change of positions'''
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
    '''Yields a generator containing lists of the current state and potential successive states'''
    st8 = st8 or self.state[:]
    for move in self.posMoves:
      nextMove = self.movement(st8, move)
      if self.isValid(nextMove):
        yield [st8, nextMove]


def process(nf, ns, bc):
  '''Yields a generator of all paths that solve the problem'''
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
    '''
    nf = number of foxes
    ns = number of sheep
    bc = boat capacity
    Makes tuple of these params for ease of use later
    '''
    self.params = (nf, ns, bc)

  def __iter__(self):
    '''Returns the generator created by process(*self.params). The same as doing process(*self.params)'''
    return process(*self.params)

  def stepForm(self, stepNum, step):
    '''Formats a step'''
    return 'Step {}: {}F {}S {}B | {}F {}S {}B'.format(stepNum, *step[0], *step[1])
    
  def solForm(self, solNum, sol):
    '''Formats a solution'''
    header = f'Solution {solNum}:\n{"-"*25}\n'
    body = '\n'.join([self.stepForm(stepNum, step) for stepNum, step in enumerate(sol)])
    tail = '\n' + '-'*25
    
    return header + body + tail
  
  def printout(self, limit=float('inf')):
    '''Prints all solutions or solutions up to a limit'''
    solList = process(*self.params)
    print('Solutions')
    print('='*25)
    for sn, s in enumerate(solList, start=1):
      print(self.solForm(sn, s))
      if sn == limit:
        break
      
  def shortest(self, acceptable=0, timeout=float('inf')):
    '''Prints the shortest solution or the first solution less than or equal to an acceptable number of steps.'''
    sols = process(*self.params)
    start = time.time()
    short = (1, next(sols))
    if time.time()-start < timeout:
      for i, v in enumerate(sols, start=2):
        if len(v) < len(short[1]):
          short = (i, v)
        if len(v)-1 <= acceptable:
          break
        if time.time()-start >= timeout:
          break
    
    print('Shortest solution')
    print('=' * 25)
    print(self.solForm(*short))


if __name__ == '__main__':
  nf = int(input('Number of foxes: '))
  ns = int(input('Number of sheep: '))
  bc = int(input('Boat capacity: '))
  sols = solutions(nf, ns, bc)
