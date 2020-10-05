from gramatica import *
import os

texto = '''E  := T Ep
Ep := + T Ep 
Ep := - T Ep
Ep := lambda
T  := F Tp
Tp := * F Tp  |  /  F Tp  | lambda
F  := ( E ) | num | id
'''

map_symbols_to_names = {"-" : "menos", "+" : "mas", "*" : "multiplicacion", "/" : "division", "(" : "parentesis_abrir", ")" : "parentesis_cerrar"}

g1 = Gramatica()
tabla_sintactica = Tabla_Sintactica()
g1.cargar(texto)
g1.crear_tabla(tabla_sintactica)

print("Tabla sintactica generada:")
print(tabla_sintactica.tabla_sintactica)
print()

print("Validar entrada:")
cadena1 = "id + id"
valido, raiz = g1.analizar_cadena(cadena1, tabla_sintactica)
print(cadena1, " => ", valido)
print()

print("Arbol sintactico de entrada:")
raiz.imprimir()
