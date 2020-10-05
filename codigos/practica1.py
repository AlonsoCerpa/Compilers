#Alonso Jesús Cerpa Salas

#Ejercicio 4
#Clase Token con miembro palabra, indice (en la linea), y tipo (E -> entero, V -> varaible, O -> operador)
class Token:
    palabra = ""
    indice = -1
    tipo = ""

    def __init__(self, palabra, indice, tipo):
        self.palabra = palabra
        self.indice = indice
        self.tipo = tipo

    #Ejercicio 5
    def imprimir(self):
        print("Token[" + self.palabra + "]: pos = " + str(self.indice) + ", tipo = " + self.tipo)

#Ejercicio 1
#Analizador lexico: Recibe una linea de codigo en forma de cadena de caracteres,
#la procesa y retorna una lista de objetos Token.
#Por ejemplo:
#Entrada: "a =tmp1+40"
#Salida: [Token("a", 0, "V"), Token("=", 2, "O"), Token("tmp1", 3, "V"), Token("+", 7, "O"), Token("40", 8, "E")]
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
                tokens.append(Token(palabra, idx_inicial, "V")) #variable
                palabra = ""
                modo = "neutro"
            #si estamos modo variable y el caracter actual es un operador, entonces el nombre de la variable terminó,
            #y se pasa al modo operador
            elif caracter in caracteres_operadores:
                tokens.append(Token(palabra, idx_inicial, "V")) #variable
                palabra = "" + caracter
                idx_inicial = idx
                modo = "operador"
            #caso contrario seguir leyendo los caracteres de la variable
            else:
                palabra += caracter

        elif modo == "numerico":
            #si estamos modo numérico y el caracter actual es " ", entonces el número entero terminó
            if caracter == " ":
                tokens.append(Token(palabra, idx_inicial, "E")) #entero
                palabra = ""
                modo = "neutro"
            #si estamos modo numérico y el caracter actual es un operador, entonces el número entero terminó,
            #y se pasa al modo operador
            elif caracter in caracteres_operadores:
                tokens.append(Token(palabra, idx_inicial, "E")) #entero
                palabra = "" + caracter
                idx_inicial = idx
                modo = "operador"
            #caso contrario seguir leyendo los caracteres del número entero
            else:
                palabra += caracter

        elif modo == "operador":
            #si estamos modo operador y el caracter actual es " ", entonces el operador terminó
            if caracter == " ":
                tokens.append(Token(palabra, idx_inicial, "O")) #operador
                palabra = ""
                modo = "neutro"
            #si estamos modo operador y el caracter actual es del alfabeto, entonces el operador terminó,
            #y se pasa al modo variable
            elif caracter in caracteres_alfabeto:
                tokens.append(Token(palabra, idx_inicial, "O")) #operador
                palabra = "" + caracter
                idx_inicial = idx
                modo = "variable"
            #si estamos modo operador y el caracter actual es numérico, entonces el operador terminó,
            #y se pasa al modo numérico
            elif caracter in caracteres_numericos:
                tokens.append(Token(palabra, idx_inicial, "O")) #operador
                palabra = "" + caracter
                idx_inicial = idx
                modo = "numerico"
            else:
                palabra += caracter
        idx += 1

    #para los casos donde queda un token al final de la linea de entrada
    if modo == "variable":
        tokens.append(Token(palabra, idx_inicial, "V")) #variable
    elif modo == "numerico":
        tokens.append(Token(palabra, idx_inicial, "E")) #entero
    elif modo == "operador":
        tokens.append(Token(palabra, idx_inicial, "O")) #operador
                
    return tokens

#Ejercicio 2 y 3

#Entrada:
#linea: linea de código en formato cadena de caracteres
#idx: índice de la linea
#Operación: Encuentra el primer número entero a partir del índice "idx" en la cadena "linea"
#y retorna el número encontrado en formato string y el índice siguiente al número encontrado
def reconoceNumero(linea, idx):
    linea = linea[idx:]
    caracteres_alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    caracteres_numericos = "0123456789"
    modo = "neutro"
    numero = ""
    for caracter in linea:
        if modo == "neutro":
            if caracter in caracteres_alfabeto:
                modo = "variable"
            elif caracter in caracteres_numericos:
                numero += caracter
                modo = "numerico"
        elif modo == "variable":
            if caracter == " ":
                modo = "neutro"

        elif modo == "numerico":
            if caracter == " ":
                return numero, idx 
            else:
                numero += caracter
        idx += 1

    return numero, idx

#Entrada:
#linea: linea de código en formato cadena de caracteres
#idx: índice de la linea
#Operación: Encuentra el primer nombre de variable a partir del índice "idx" en la cadena "linea"
#y retorna el nombre de variable encontrado en formato string y el índice siguiente al nombre de variable encontrado
def reconoceVariable(linea, idx):
    linea = linea[idx:]
    caracteres_alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    caracteres_numericos = "0123456789"
    modo = "neutro"
    variable = ""
    for caracter in linea:
        if modo == "neutro":
            if caracter in caracteres_alfabeto:
                variable += caracter
                modo = "variable"
            elif caracter in caracteres_numericos:
                modo = "numerico"
        elif modo == "variable":
            if caracter == " ":
                return variable, idx
            else:
                variable += caracter

        elif modo == "numerico":
            if caracter == " ":
                modo = "neutro"

        idx += 1

    return variable, idx


def main():
    #Ejercicio 1, 4 y 5
    linea = "  var1=Tmp0 +  20+24"
    print("Linea = ", linea)
    tokens = analizadorLexico(linea)
    for token in tokens:
        token.imprimir()
    print()

    #Ejercicio 2 y 3
    linea = "var1 = Tmp0 + 20 + 24"
    print("Linea = ", linea)
    idx = 0
    numero, idx = reconoceNumero(linea, idx)
    print("Numero = ", numero)
    print("Indice = ", idx)
    numero, idx = reconoceNumero(linea, idx)
    print("Numero = ", numero)
    print("Indice = ", idx)

    idx = 0
    variable, idx = reconoceVariable(linea, idx)
    print("Variable = ", variable)
    print("Indice = ", idx)
    variable, idx = reconoceVariable(linea, idx)
    print("Variable = ", variable)
    print("Indice = ", idx)

main()