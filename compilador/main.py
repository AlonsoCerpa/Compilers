#Alumno: Alonso Jesús Cerpa Salas

from gramatica import *
from analizador_lexico import *
import os
import pandas as pd

with open('gramatica.txt', 'r') as file:
    texto = file.read()

g1 = Gramatica()
tabla_sintactica = Tabla_Sintactica()
g1.cargar(texto)
g1.crear_tabla(tabla_sintactica)

#print("Tabla sintactica generada:")
#print(tabla_sintactica.tabla_sintactica)
#print()

cadena1 = "res =    25    * 2.0"

print("Analizador Lexico")
tokens = analizadorLexico(cadena1)
entrada = construir_entrada(tokens)

for token in tokens:
    token.imprimir()
print()

print("Validar entrada:")
valido, raiz = g1.analizar_cadena(entrada, tabla_sintactica, tokens)
print(cadena1, " => ", valido)
print()

#print("Arbol sintactico de entrada:")
#raiz.imprimir()
#print()

print("Interpretador")
stack = []
buffer_variables = {}
raiz.interpret(stack, buffer_variables)
print("Cadena de entrada: ", cadena1)
print("Buffer de variables = ", buffer_variables)
print()
