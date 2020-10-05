#Alumno: Alonso Jesús Cerpa Salas

#Nota: El texto de entrada para el metodo "cargar()"" de la clase "Gramatica"
#debe empezar con el no-terminal inicial

import pprint #para imprimir la tabla sintactica ordenadamente
from collections import deque

class Gramatica:
    def __init__(self):
        self.primer_no_terminal = ""
        self.producciones = {}   #diccionario de listas de listas
        self.terminales = set()  #set utiliza una función hash para que la búsqueda sea O(1)
        self.no_terminales = set()
        self.tabla_sintactica = {}  #es un diccionario de diccionarios de listas
        
    def cargar(self, texto):
        #Agrega las producciones
        primer_no_terminal_configurado = False
        for line in texto.splitlines():
            cadenas = line.split()
            cabeza_produccion = cadenas[0]
            if primer_no_terminal_configurado == False:
                self.primer_no_terminal = cabeza_produccion
                primer_no_terminal_configurado = True
            if cabeza_produccion not in self.producciones:
                self.producciones[cabeza_produccion] = []
            end_idx = len(cadenas)
            if "|" in cadenas:
                end_idx = cadenas.index("|")
            start_idx = 2
            while True:
                cuerpo_produccion = []
                for i in range(start_idx, end_idx):
                    cuerpo_produccion.append(cadenas[i])
                self.producciones[cabeza_produccion].append(cuerpo_produccion)
                if end_idx == len(cadenas):
                    break
                start_idx = end_idx + 1
                end_idx_old = end_idx
                end_idx = len(cadenas)
                if "|" in cadenas[end_idx_old+1: ]:
                    end_idx = end_idx_old + 1
                    end_idx += cadenas[end_idx_old+1: ].index("|")

        #Agrega los no terminales
        for cabeza_produccion in self.producciones:
            self.no_terminales.add(cabeza_produccion)
            
        #Agrega los terminales
        for _, cuerpos_produccion in self.producciones.items():
            for cuerpo in cuerpos_produccion:
                for simbolo in cuerpo:
                    if simbolo not in self.no_terminales:
                        self.terminales.add(simbolo)
                    
    def get_produccion(self, cabeza_produccion):
        return self.producciones.get(cabeza_produccion)
    
    def get_producciones(self):
        return self.producciones

    def get_primeros(self):
        primeros = {}
        for no_term in self.no_terminales:
            primeros[no_term] = self.get_primero(no_term)
        return primeros

    def get_primero(self, no_term, dict_idx_cuerpo=None):
        primero = set()
        cuerpos_produccion = self.get_produccion(no_term)
        for idx, cuerpo in enumerate(cuerpos_produccion):
            if cuerpo[0] in self.terminales:
                if dict_idx_cuerpo != None:
                    dict_idx_cuerpo[cuerpo[0]] = idx
                primero.add(cuerpo[0])
            else:
                primero_aux = self.get_primero(cuerpo[0])
                for prim in primero_aux:
                    if dict_idx_cuerpo != None:
                        dict_idx_cuerpo[prim] = idx
                    primero.add(prim)
        return primero

    def get_siguientes(self):
        siguientes = {}
        for no_term in self.no_terminales:
            siguientes[no_term] = set()

        for no_term in self.no_terminales:
            self.process_siguiente(no_term, siguientes)
        return siguientes

    def process_siguiente(self, no_term, siguientes):
        if len(siguientes[no_term]) != 0:
            return
        else:
            if no_term == self.primer_no_terminal:
                siguientes[no_term].add("$")
            for no_term_cabeza, cuerpos_produccion in self.producciones.items():
                for cuerpo in cuerpos_produccion:
                    for idx, simbolo in enumerate(cuerpo):
                        if simbolo == no_term:
                            if idx < len(cuerpo) - 1:
                                if cuerpo[idx+1] in self.terminales:
                                    siguientes[no_term].add(cuerpo[idx+1])
                                else:
                                    primero_aux = self.get_primero(cuerpo[idx+1])
                                    for prim in primero_aux:
                                        if prim != "lambda":
                                            siguientes[no_term].add(prim)
                                        else:
                                            self.process_siguiente(cuerpo[idx+1], siguientes)
                                            for sig in siguientes[cuerpo[idx+1]]:
                                                siguientes[no_term].add(sig)
                            else:
                                if no_term != no_term_cabeza:
                                    self.process_siguiente(no_term_cabeza, siguientes)
                                    for sig in siguientes[no_term_cabeza]:
                                        siguientes[no_term].add(sig)

    def imprimir(self):
        for cabeza_produccion, cuerpos_produccion in self.producciones.items():
            for cuerpo in cuerpos_produccion:
                print(cabeza_produccion + " := ", end="")
                for simbolo in cuerpo:
                    print(simbolo + " ", end="")
                print()

    def crear_tabla(self):
        siguientes = self.get_siguientes()
        for no_terminal in self.no_terminales:
            self.tabla_sintactica[no_terminal] = {}
            dict_idx_cuerpo = {}
            for primero in self.get_primero(no_terminal, dict_idx_cuerpo):
                if primero != "lambda":
                    self.tabla_sintactica[no_terminal][primero] = self.producciones[no_terminal][dict_idx_cuerpo[primero]]
                else:
                    for siguiente in siguientes[no_terminal]:
                        self.tabla_sintactica[no_terminal][siguiente] = ["lambda"]
    
    def analizar_cadena(self, cadena):
        entrada = deque()
        string1 = ""
        string_active = False
        for caracter in cadena:
            if caracter != " ":
                if string_active == False:
                    string1 = ""
                    string_active = True
                string1 += caracter
            else:
                if string_active == True:
                    string_active = False
                    entrada.append(string1)
        if string_active == True:
            entrada.append(string1)
        entrada.append("$")

        pila = deque()
        pila.append("$")
        pila.append(self.primer_no_terminal)

        while len(entrada) != 0 and len(pila) != 0:
            if entrada[0] == pila[-1]:
                entrada.popleft()
                pila.pop()
            else:
                tmp = pila.pop()
                fila_tabla = self.tabla_sintactica.get(tmp)
                if fila_tabla != None:
                    simbolos = fila_tabla.get(entrada[0])
                    if simbolos != None:
                        for simbolo in reversed(simbolos):
                            if simbolo != "lambda":
                                pila.append(simbolo)
        
        return len(entrada) == 0 and len(pila) == 0
    
    def llenar_estaticamente_tabla_sintactica(self):
        tabla_sintactica = {}
        tabla_sintactica["E"] = {"(": ["T", "Ep"], "num": ["T", "Ep"], "id": ["T", "Ep"]}
        tabla_sintactica["Ep"] = {"+": ["+", "T", "Ep"], "-": ["-", "T", "Ep"], ")": ["lambda"], "$": ["lambda"]}
        tabla_sintactica["T"] = {"(": ["F", "Tp"], "num": ["F", "Tp"], "id": ["F", "Tp"]}
        tabla_sintactica["Tp"] = {"+": ["lambda"], "-": ["lambda"], "*": ["*", "F", "Tp"], "/": ["/", "F", "Tp"], ")": ["lambda"], "$": ["lambda"]}
        tabla_sintactica["F"] = {"(": ["(", "E", ")"], "num": ["num"], "id": ["id"]}
        return tabla_sintactica

texto = '''E  := T Ep
Ep := + T Ep 
Ep := - T Ep
Ep := lambda
T  := F Tp
Tp := * F Tp  |  /  F Tp  | lambda
F  := ( E ) | num | id
'''
g1 = Gramatica()
g1.cargar(texto)

print("Algunas producciones de la gramatica:")
print("Ep :=", g1.get_produccion("Ep"))
print("Tp :=", g1.get_produccion("Tp"))
print()

print("No terminales =", g1.no_terminales)
print("Terminales =", g1.terminales)
print()

print("Gramatica:")
g1.imprimir()
print()

print("Tabla sintactica:")
tabla_sintactica1 = g1.llenar_estaticamente_tabla_sintactica()
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(tabla_sintactica1)
print()

print("Primeros:")
primeros = g1.get_primeros()
print(primeros)
print()

print("Siguientes:")
siguientes = g1.get_siguientes()
print(siguientes)
print()

print("Tabla sintactica:")
g1.crear_tabla()
tabla_sintactica2 = g1.tabla_sintactica
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(tabla_sintactica2)
print()

if tabla_sintactica1 == tabla_sintactica2:
    print("La tabla sintactica automatica es igual a la estatica")
else:
    print("La tabla sintactica automatica es diferente a la estatica")
print()

print("Analizando las siguientes cadena")
cadena1 = "num + num + num + num"
print(cadena1, " => ", g1.analizar_cadena(cadena1))
cadena2 = "( num + num ) + ( num + num )"
print(cadena2, " => ", g1.analizar_cadena(cadena2))
cadena3 = "num * ( num * num )"
print(cadena3, " => ", g1.analizar_cadena(cadena3))
cadena4 = "( num * ) num"
print(cadena4, " => ", g1.analizar_cadena(cadena4))
print()