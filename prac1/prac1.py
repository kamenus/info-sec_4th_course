import random
 
def is_Prime(n, trials_count):
  default_primes = [2, 3, 5, 7]
  default_composite = [0, 1, 4, 6, 8, 9]

  if n in default_composite:
    return False

  if n in default_primes:
    return True

  s = 0
  d = n-1

  while d%2==0:
    d>>=1
    s+=1

  def trial_composite(a):
    if pow(a, d, n) == 1:
      return False
    for i in range(s):
      if pow(a, 2**i * d, n) == n-1:
        return False
    return True  

  for i in range(trials_count):
    a = random.randrange(2, n)

    if trial_composite(a):
      return False

  return True  

if __name__ == '__main__':
  n = int(input('Введите число: '))
  trials_count = 8
  print(is_Prime(n, trials_count))
