import random
import math

def primesInRange(x, y):
  prime_list = []

  for n in range(x, y):
    isPrime = True

    for num in range(2, n):
      if n % num == 0:
        isPrime = False

    if isPrime:
      prime_list.append(n)
          
  return prime_list

# actual code

def eulers_func (n_public):
  return (p - 1) * (q - 1)

def get_private_key(el, module):

  def gcdExtended(module, el):
    if module == 0:
      return el,0,1
    gcd,x1,y1 = gcdExtended(el % module, module)
    x = y1 - (el // module) * x1
    y = x1
    return gcd,x,y

  gcd, x, y = gcdExtended(module, el)

  if gcd == 1:
    return (x % el + el) % el
  else:
    return -1

def get_random_Primes(start, end):
  primes = primesInRange(10, 300)
  random.shuffle(primes)
  return primes[0], primes[1]

p, q = get_random_Primes(10, 300)

def get_e(f):
  primes = get_random_Primes(2, f - 1)

  for i in primes:
    if (math.gcd(i, f) == 1):
      return i

n_public = p * q
f = eulers_func(n_public)

e_public = get_e(f)

private_key = get_private_key(f, e_public) # d

message = 11

encrypted_message = message ** e_public % n_public

decrypted_message = encrypted_message ** private_key % n_public

print(message)
print(encrypted_message)
print(decrypted_message)
