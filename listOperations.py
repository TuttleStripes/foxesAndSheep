def add(*args):
  return sum(args)
  
def sub(*args):
  dif = args[0]
  for i in args[1:]:
    dif -= i
  return dif

def mult(*args):
  product = args[0]
  for i in args[1:]:
    product *= i
  return product

def div(*args):
  quotient = args[0]
  for i in args[1:]:
    quotient /= i
  return quotient


def funcLists(func, *lists): 
  return map(func, *lists)

  
