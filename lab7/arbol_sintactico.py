class NodoArbolSintactico:
    def __init__(self, _etiqueta, _padre=None, _siguiente=None):
        self.etiqueta = _etiqueta
        self.hijos = []
        self.padre = _padre
        self.siguiente = _siguiente

    def imprimir(self):
        print(self.etiqueta, " -> ", end="")
        for hijo in self.hijos:
            print(hijo.etiqueta, end=" ")
        print()
        for hijo in self.hijos:
            hijo.imprimir()
        
def operacion1(nodo, simbolos_hijos):
    if nodo != None:
        for simbolo_hijo in simbolos_hijos:
            nodo.hijos.append(NodoArbolSintactico(simbolo_hijo, nodo))
        for idx, hijo in enumerate(nodo.hijos):
            if idx < len(nodo.hijos)-1:
                hijo.siguiente = nodo.hijos[idx+1]
        return nodo.hijos[0]
    else:
        return None

def operacion2(nodo):
    if nodo != None:
        if nodo.siguiente != None:
            return nodo.siguiente
        else:
            if nodo.padre != None:
                return operacion2(nodo.padre)
            else:
                return None
    else:
        return None

def operacion3(nodo):
    if nodo != None:
        nodo.hijos.append(NodoArbolSintactico("lambda", nodo))
        return operacion2(nodo)
    else:
        return None
