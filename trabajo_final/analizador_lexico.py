#Analizador lexico: Recibe una linea de codigo en forma de cadena de caracteres,
#la procesa y retorna una lista de objetos Token.

from collections import deque

class Token:
    palabra = ""
    indice = -1
    tipo = ""

    def __init__(self, palabra, indice, tipo):
        self.palabra = palabra
        self.indice = indice
        self.tipo = tipo

    def imprimir(self):
        print("Token[" + self.palabra + "]: pos = " + str(self.indice) + ", tipo = " + self.tipo)

def analizadorLexico(linea):
    tokens = []
    caracteres_alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    caracteres_numericos = "0123456789"
    caracteres_operadores = "+-*/="
    modo = "neutro"
    palabra = ""
    idx_inicial = 0
    idx = 0
    for caracter in linea:
        #Si esta en modo neutro, busca si el caracter actual es del alfabeto para pasar al modo variable,
        #o si el caracter actual es numérico para pasar al modo numérico,
        #o si el caracter actual es de operador para pasar al modo operador
        if modo == "neutro":
            if caracter in caracteres_alfabeto:
                palabra += caracter
                idx_inicial = idx
                modo = "variable"
            elif caracter in caracteres_numericos:
                palabra += caracter
                idx_inicial = idx
                modo = "numerico"
            elif caracter in caracteres_operadores:
                palabra += caracter
                idx_inicial = idx
                modo = "operador"
        elif modo == "variable":
            #si estamos modo variable y el caracter actual es " ", entonces el nombre de la variable terminó
            if caracter == " ":
                tokens.append(Token(palabra, idx_inicial, "Name")) #variable
                palabra = ""
                modo = "neutro"
            #si estamos modo variable y el caracter actual es un operador, entonces el nombre de la variable terminó,
            #y se pasa al modo operador
            elif caracter in caracteres_operadores:
                tokens.append(Token(palabra, idx_inicial, "Name")) #variable
                palabra = "" + caracter
                idx_inicial = idx
                modo = "operador"
            #caso contrario seguir leyendo los caracteres de la variable
            else:
                palabra += caracter

        elif modo == "numerico" or modo == "flotante":
            #si estamos modo numérico y el caracter actual es " ", entonces el número entero terminó
            if caracter == " ":
                if modo == "flotante":
                    tokens.append(Token(palabra, idx_inicial, "FLOAT")) #flotante
                else:
                    tokens.append(Token(palabra, idx_inicial, "INT")) #entero
                palabra = ""
                modo = "neutro"
            #si estamos modo numérico y el caracter actual es un operador, entonces el número entero terminó,
            #y se pasa al modo operador
            elif caracter in caracteres_operadores:
                if modo == "flotante":
                    tokens.append(Token(palabra, idx_inicial, "FLOAT")) #flotante
                else:
                    tokens.append(Token(palabra, idx_inicial, "INT")) #entero
                palabra = "" + caracter
                idx_inicial = idx
                modo = "operador"

            elif caracter == ".":
                if modo == "numerico":
                    modo = "flotante"
                else:
                    raise ValueError('Error Lexico: Mas de un punto en un FLOAT')
                palabra += caracter

            #caso contrario seguir leyendo los caracteres del número entero
            else:
                palabra += caracter

        elif modo == "operador":
            #si estamos modo operador y el caracter actual es " ", entonces el operador terminó
            if caracter == " ":
                tokens.append(Token(palabra, idx_inicial, palabra)) #operador
                palabra = ""
                modo = "neutro"
            #si estamos modo operador y el caracter actual es del alfabeto, entonces el operador terminó,
            #y se pasa al modo variable
            elif caracter in caracteres_alfabeto:
                tokens.append(Token(palabra, idx_inicial, palabra)) #operador
                palabra = "" + caracter
                idx_inicial = idx
                modo = "variable"
            #si estamos modo operador y el caracter actual es numérico, entonces el operador terminó,
            #y se pasa al modo numérico
            elif caracter in caracteres_numericos:
                tokens.append(Token(palabra, idx_inicial, palabra)) #operador
                palabra = "" + caracter
                idx_inicial = idx
                modo = "numerico"
            else:
                palabra += caracter
        idx += 1

    #para los casos donde queda un token al final de la linea de entrada
    if modo == "variable":
        tokens.append(Token(palabra, idx_inicial, "Name")) #variable
    elif modo == "numerico":
        tokens.append(Token(palabra, idx_inicial, "INT")) #entero
    elif modo == "flotante":
        tokens.append(Token(palabra, idx_inicial, "FLOAT")) #flotante
    elif modo == "operador":
        tokens.append(Token(palabra, idx_inicial, palabra)) #operador
                
    return tokens

def construir_entrada(tokens):
    entrada = deque()
    for token in tokens:
        entrada.append(token.tipo)
    entrada.append("$")

    return entrada

