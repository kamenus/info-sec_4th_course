import re
alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def getDictionary(source_symbols, encoded_symbols):
  dictionary = {}
  for i in range(len(source_symbols)):
    dictionary[encoded_symbols[i][0]] = source_symbols[i][0]
  return dictionary

def readText():
  file = open("First_tome.txt")
  text = file.read().lower()
  # text = "мы с тамарой ходим парой"

  return text

def getCaesar(step, text):
  decode_text = ''

  for sym in text:
    if sym.isalpha():
      decode_text += alphabet[(alphabet.find(sym) + step) % 33]
    else:
      decode_text += sym

  return decode_text

def decodeViaMonogram(text, decode_text):
  monograms_text = {}
  regex_string = r'[абвгдеёжзийклмнопрстуфхцчшщъыьэюя]{1}'
  p = re.compile(regex_string)

  for i in p.findall(text):
    if i in monograms_text:
      monograms_text[i] += 1
    else:
      monograms_text[i] = 1

  monograms_decode_text = {}

  p = re.compile(regex_string)

  for i in p.findall(decode_text):
    if i in monograms_decode_text:
      monograms_decode_text[i] += 1
    else:
      monograms_decode_text[i] = 1

  list_monograms_text = list(monograms_text.items())
  list_monograms_text.sort(key=lambda i: i[1])

  list_monograms_decode_text = list(monograms_decode_text.items())
  list_monograms_decode_text.sort(key=lambda i: i[1])

  dictionary = getDictionary(list_monograms_text, list_monograms_decode_text)

  result = re.compile(r'.{1}').findall(decode_text)
  for i in range(len(result)):
    if result[i] in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
      symbol_from_dict = dictionary[result[i]]
      if symbol_from_dict:
        result[i] = symbol_from_dict

  return "".join(result)

def decodeViaBigram(text, encoded_text):
  text_symbols = re.compile(r'.{1}').findall(text)
  encoded_text_symbols = re.compile(r'.{1}').findall(encoded_text)

  source_quantity = getSymbolQuantity(text_symbols)
  encoded_quantity = getSymbolQuantity(encoded_text_symbols)

  source_list = list(source_quantity.items())
  encoded_list = list(encoded_quantity.items())
  source_list.sort(key=lambda i: i[1])
  encoded_list.sort(key=lambda i: i[1])

  dictionary = getDictionary(source_list, encoded_list)
  # print(dictionary)

  current = []
  result = encoded_text_symbols

  for encoded_index in range(len(result)):
    encoded_symbol = result[encoded_index]

    if len(current) < 2:
      if (encoded_symbol in alphabet):
        current.append([encoded_index, encoded_symbol])
    else:
      str_from_dict = ""
      for symbol_to_process in current:
        str_from_dict += symbol_to_process[1]

      result_str = dictionary[str_from_dict]
      for i in range(len(result_str)):
        result[current[i][0]] = result_str[i]

      if (encoded_symbol in alphabet):
        current = [[encoded_index, encoded_symbol]]

  if len(current) == 2:
    str_from_dict = ""
    for symbol_to_process in current:
      str_from_dict += symbol_to_process[1]

    result_str = dictionary[str_from_dict]
    for i in range(len(result_str)):
      result[current[i][0]] = result_str[i]
  
  return "".join(result)

def getSymbolQuantity(text_array):
  dictionary = {}
  current = ""

  for i in text_array:
    if len(current) < 2:
      if i in alphabet:
        current += i
    else:
      if current in dictionary:
        dictionary[current] += 1
      else:
        dictionary[current] = 1
      if i in alphabet:
        current = i

  return dictionary

if __name__ == '__main__':
  text = readText()

  encrypted_text = getCaesar(5, text)

  result1 = decodeViaMonogram(text, encrypted_text)
  result2 = decodeViaBigram(text, encrypted_text)
  file = open("result.txt", "w")
  text = file.write(result1)
  print(result1, result2)
