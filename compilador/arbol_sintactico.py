class NodoArbolSintactico:
    def __init__(self, _etiqueta, _value="", _padre=None, _siguiente=None):
        self.etiqueta = _etiqueta
        self.value = _value
        self.pos = -1
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

    def interpret(self, stack, buffer_variables, flag=False):
        if self.etiqueta == "Name":
            stack.append(("Name", self.value, self.pos))
            for hijo in self.hijos:
                hijo.interpret(stack, buffer_variables, True)
        elif self.etiqueta == "=":
            if stack[-1][0] == ("Name"):
                stack.append(("Action", "Assign", self.pos))
            for hijo in self.hijos:
                hijo.interpret(stack, buffer_variables, True)
        elif self.etiqueta == "INT" or self.etiqueta == "FLOAT":
            if stack[-1][1] == "Assign" or stack[-1][0] == "BinOp":
                stack.append((self.etiqueta, self.value, self.pos))
            for hijo in self.hijos:
                hijo.interpret(stack, buffer_variables, True)
        elif self.etiqueta == "*" or self.etiqueta == "+" or self.etiqueta == "-" or self.etiqueta == "/":
            if stack[-1][0] == "INT" or stack[-1][0] == "FLOAT":
                stack.append(("BinOp", self.etiqueta, self.pos))
            for hijo in self.hijos:
                hijo.interpret(stack, buffer_variables, True)
        else:
            for hijo in self.hijos:
                hijo.interpret(stack, buffer_variables, True)

        if flag == False:
            if len(stack) > 0:
                if stack[0][0] == "Name":
                    if stack[1][1] == "Assign":
                        name_var = stack[0][1]
                        stack.pop(0)
                        stack.pop(0)
                        value_assign = 0.0
                        curr_op = ""
                        found_float = False
                        found_int = False
                        while len(stack) > 0:
                            tup = stack.pop(0)
                            if tup[0] == "INT":
                                found_int = True
                                if curr_op == "":
                                    value_assign = int(tup[1])
                                elif curr_op == "*":
                                    value_assign *= int(tup[1])
                                elif curr_op == "+":
                                    value_assign += int(tup[1])
                                elif curr_op == "-":
                                    value_assign -= int(tup[1])
                                elif curr_op == "/":
                                    if int(tup[1]) == 0:
                                        str_err = 'Error in pos %d: No se puede dividir por 0' % (tup[2])
                                        raise ValueError(str_err)
                                    value_assign /= int(tup[1])
                            elif tup[0] == "FLOAT":
                                found_float = True
                                if curr_op == "":
                                    value_assign = float(tup[1])
                                elif curr_op == "*":
                                    value_assign *= float(tup[1])
                                elif curr_op == "+":
                                    value_assign += float(tup[1])
                                elif curr_op == "-":
                                    value_assign -= float(tup[1])
                                elif curr_op == "/":
                                    if float(tup[1]) == 0.0:
                                        str_err = 'Error in pos %d: No se puede dividir por 0.0' % (tup[2])
                                        raise ValueError(str_err)
                                    value_assign /= float(tup[1])
                            elif tup[0] == "BinOp":
                                curr_op = tup[1]
                        if found_int and found_float:
                            print("WARNING: Int y Float encontrados en operacion binaria, Int convertido a Float")
                        buffer_variables[name_var] = value_assign
            
def operacion1(nodo, simbolos_hijos):
    if nodo != None:
        for simbolo_hijo in simbolos_hijos:
            nodo.hijos.append(NodoArbolSintactico(simbolo_hijo, "", nodo))
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
        nodo.hijos.append(NodoArbolSintactico("lambda", "", nodo))
        return operacion2(nodo)
    else:
        return None
