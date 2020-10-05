#Alumno: Alonso Jesús Cerpa Salas

import pprint #para imprimir la tabla sintactica ordenadamente

class Gramatica:
    def __init__(self):
        self.producciones = {}   #diccionario
        self.terminales = set()  #set utiliza una función hash para que la búsqueda sea O(1)
        self.no_terminales = set()
        self.tabla_sintactica = {}  #es un diccionario de diccionarios de listas
        
    def cargar(self, texto):
        #Agrega las producciones
        for line in texto.splitlines():
            cadenas = line.split()
            cabeza_produccion = cadenas[0]
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

    def imprimir(self):
        for cabeza_produccion, cuerpos_produccion in self.producciones.items():
            for cuerpo in cuerpos_produccion:
                print(cabeza_produccion + " := ", end="")
                for simbolo in cuerpo:
                    print(simbolo + " ", end="")
                print()
    
    def llenar_estaticamente_tabla_sintactica(self):
        self.tabla_sintactica["E"] = {"(": ["T", "Ep"], "num": ["T", "Ep"], "id": ["T", "Ep"]}
        self.tabla_sintactica["Ep"] = {"+": ["+", "T", "Ep"], "-": ["-", "T", "Ep"], ")": ["lambda"], "$": ["lambda"]}
        self.tabla_sintactica["T"] = {"(": ["F", "Tp"], "num": ["F", "Tp"], "id": ["F", "Tp"]}
        self.tabla_sintactica["Tp"] = {"+": ["lambda"], "-": ["lambda"], "*": ["*", "F", "Tp"], "/": ["/", "F", "Tp"], ")": ["lambda"], "$": ["lambda"]}
        self.tabla_sintactica["F"] = {"(": ["(", "E", ")"], "num": ["num"], "id": ["id"]}

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
g1.llenar_estaticamente_tabla_sintactica()
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(g1.tabla_sintactica)