def custom_hash(key):
  mask = 0x0000FFFF
  hash = 0

  for i in range(len(key)):
    hash = hash + (ord(key[i]) ** i)
    hash = (hash << 2) & mask

  return hash

if __name__ == '__main__':
  key = input('Enter key: ')
  print(custom_hash(key))
