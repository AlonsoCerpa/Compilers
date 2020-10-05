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
g1.cargar(texto)
g1.crear_tabla()

nombre_carpeta_archivos_gen = "archivos_generados"
os.mkdir(nombre_carpeta_archivos_gen)

for terminal in g1.terminales:
    nombre_terminal = map_symbols_to_names.get(terminal, terminal)
    f = open(nombre_carpeta_archivos_gen + "/Terminal_" + nombre_terminal + ".py", "w")
    write_text0 = "class Terminal_" + nombre_terminal + "(AbstractExpressionT):\n"
    write_text1 = "    #valor\n" 
    write_text2 = "    def​ interprets():\n"
    write_text3 = "        return valor\n"
    f.write(write_text0)
    f.write(write_text1)
    f.write(write_text2)
    f.write(write_text3)
    
    f.close()

for no_terminal in g1.no_terminales:
    nombre_no_terminal = map_symbols_to_names.get(no_terminal, no_terminal)
    f = open(nombre_carpeta_archivos_gen + "/No_terminal_" + nombre_no_terminal + ".py", "w")
    write_text0 = "class No_terminal_" + nombre_no_terminal + "(AbstractExpressionNT):\n"
    write_text1 = "    #diccionario<NombreClase, Objeto >\n" 
    write_text2 = "    def​ interprets(val1,val2,val3):\n"
    write_text3 = "        return (0,0,0)\n"
    f.write(write_text0)
    f.write(write_text1)
    f.write(write_text2)
    f.write(write_text3)
    
    f.close()
    