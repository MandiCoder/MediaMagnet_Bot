import random

def generateWord(length:str) -> str:
  """
  La función genera una palabra aleatoria de una longitud específica usando letras minúsculas.
  
  :param `length`: El parámetro de longitud es un número entero que especifica la longitud deseada de la
  palabra generada
  :return: una palabra generada aleatoriamente de la longitud especificada.
  """


  letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
             'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

  word = ''
  for i in range(length):
    word += random.choice(letters)

  return word