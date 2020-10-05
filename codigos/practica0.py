#Práctica 0 - Procesamiento de texto
#Alumno: Alonso Jesús Cerpa Salas

##############################################Ejercicio 1##################################################
def verificar_balanceo(caracteres_balanceo_abierto, caracteres_balanceo_cerrado, linea_de_texto):
    pila = []

    for caracter in linea_de_texto:
        idx = caracteres_balanceo_abierto.find(caracter)
        if idx != -1:
            pila.append(caracteres_balanceo_cerrado[idx])
        else:
            idx = caracteres_balanceo_cerrado.find(caracter)
            if idx != -1:
                if len(pila) == 0:  #si se encontró un caracter cerrado que nadie lo abrió al inicio
                    return False
                else:
                    caract_de_pila = pila.pop(-1)
                    if caract_de_pila != caracter: #si se encontró un caracter cerrado que no corresponde al caracter cerrado que debería cerrar
                        return False
            else: #cualquier otro caracter
                pass

    if len(pila) != 0:  #si faltan caracteres cerrados que cierren los caracteres abiertos
        return False
    else:
        return True

##############################################Ejercicio 2##################################################
def encontrar_elemento_en_lista(elemento, lista):
    try:
        idx = lista.index(elemento)
        return idx
    except ValueError:
        return -1

def verificar_verbo_y_gerundio(verbo, gerundio):
    terminaciones_verbos = ["ar", "er", "ir"]
    terminaciones_gerundios_normal = ["ando", "iendo", "iendo"]
    verbos_casos_especiales = ["morir", "reir", "ir"]
    gerundios_casos_especiales = ["muriendo", "riendo", "yendo"]
    vocales = "aeiou"

    idx_term = encontrar_elemento_en_lista(verbo[-2:], terminaciones_verbos)
    if idx_term == -1:  #si no es verbo
        return False
    else:
        idx_vce = encontrar_elemento_en_lista(verbo, verbos_casos_especiales)
        if idx_vce != -1:  #si es verbo de caso especial
            gerundio_encontrado = gerundios_casos_especiales[idx_vce]
            if gerundio == gerundio_encontrado:
                return True
            else:
                return False
        else:
            #si el verbo tiene 3 letras o más, termina en "er" o "ir", y la 3era última letra es vocal, y el gerundio termina en "yendo"
            if len(verbo) >= 3 and (idx_term == 1 or idx_term == 2) and verbo[-3] in vocales and verbo[:-2] + "yendo" == gerundio:
                return True
            else:
                if verbo[:-2] + terminaciones_gerundios_normal[idx_term] == gerundio:
                    return True
                else:
                    return False

##############################################Ejercicio 3##################################################
def encontrar_occurrencias_de_caracter(cadena, caracter_buscado):
    ocurrencias = []
    i = 0
    for caract in cadena:
        if caract == caracter_buscado:
            ocurrencias.append(i)
        i += 1
    return ocurrencias

def encontrar_longitud_de_numero_en_cadena(cadena):
    caract_de_numeros = "0123456789."
    i = 0
    for caract in cadena:
        if caract not in caract_de_numeros:
            return i
        i += 1
    return i

def resolver_problemas_de_fisica(nombre_de_archivo):
    conceptos = ["P", "U", "I"]
    prefijos = ["m", "k", "M"]
    unidades = ["W", "V", "A"]
    with open(nombre_de_archivo, "r") as archivo:
        lineas = archivo.readlines()
        numero_de_problemas = int(lineas[0][:-1])
        for i in range(numero_de_problemas):
            linea = lineas[i+1][:-1]
            ocurrencias = encontrar_occurrencias_de_caracter(linea, "=")
            concepto1 = linea[ocurrencias[0] - 1]
            concepto2 = linea[ocurrencias[1] - 1]
            longitud_num1 = encontrar_longitud_de_numero_en_cadena(linea[ocurrencias[0]+1:])
            longitud_num2 = encontrar_longitud_de_numero_en_cadena(linea[ocurrencias[1]+1:])
            cantidad1 = linea[ocurrencias[0]+1 : ocurrencias[0]+1+longitud_num1]
            cantidad2 = linea[ocurrencias[1]+1 : ocurrencias[1]+1+longitud_num2]
            aux1 = linea[ocurrencias[0] + 1 + longitud_num1]
            aux2 = linea[ocurrencias[1] + 1 + longitud_num2]
            prefijo1 = ""
            prefijo2 = ""
            unidad1 = ""
            unidad2 = ""
            if aux1 in prefijos:
                prefijo1 = aux1
                unidad1 = linea[ocurrencias[0] + 2 + longitud_num1]
            else:
                unidad1 = aux1
            if aux2 in prefijos:
                prefijo2 = aux2
                unidad2 = linea[ocurrencias[1] + 2 + longitud_num2]
            else:
                unidad2 = aux2

            cantidad1_float = float(cantidad1)
            cantidad2_float = float(cantidad2)
            if prefijo1 == "m":
                cantidad1_float *= 0.001
            elif prefijo1 == "k":
                cantidad1_float *= 1000.0
            elif prefijo1 == "M":
                cantidad1_float *= 1000000.0

            if prefijo2 == "m":
                cantidad2_float *= 0.001
            elif prefijo2 == "k":
                cantidad2_float *= 1000.0
            elif prefijo2 == "M":
                cantidad2_float *= 1000000.0

            if concepto1 == "P" and concepto2 == "U":
                concepto_resultante = "I"
                cantidad_resultante_float = cantidad1_float / cantidad2_float
                unidad_resultante = "A"
            elif concepto1 == "U" and concepto2 == "P":
                concepto_resultante = "I"
                cantidad_resultante_float = cantidad2_float / cantidad1_float
                unidad_resultante = "A"
            elif concepto1 == "P" and concepto2 == "I":
                concepto_resultante = "U"
                cantidad_resultante_float = cantidad1_float / cantidad2_float
                unidad_resultante = "V"
            elif concepto1 == "I" and concepto2 == "P":
                concepto_resultante = "U"
                cantidad_resultante_float = cantidad2_float / cantidad1_float
                unidad_resultante = "V"
            elif concepto1 == "U" and concepto2 == "I":
                concepto_resultante = "P"
                cantidad_resultante_float = cantidad2_float * cantidad1_float
                unidad_resultante = "W"
            elif concepto1 == "I" and concepto2 == "U":
                concepto_resultante = "P"
                cantidad_resultante_float = cantidad2_float * cantidad1_float
                unidad_resultante = "W"

            print("Problem #" + str(i+1))
            print(concepto_resultante + "=", "%.2f" % cantidad_resultante_float, unidad_resultante, sep="")
            print()



def main():
    ##############################################Ejercicio 1##################################################
    print("Ejercicio 1")

    caracteres_de_balanceo_abiertos = "[("
    caracteres_de_balanceo_cerrados = "])"
    linea_de_texto = "([]) []"

    resultado_ejer1 = verificar_balanceo(caracteres_de_balanceo_abiertos, caracteres_de_balanceo_cerrados, linea_de_texto)
    if resultado_ejer1 == False:
        print("NO")
    else:
        print("SI")
    
    print()

    ##############################################Ejercicio 2##################################################
    print("Ejercicio 2")

    verbo = "huir"
    gerundio = "huyendo"

    resultado_ejer2 = verificar_verbo_y_gerundio(verbo, gerundio)
    if resultado_ejer2 == False:
        print("NO")
    else:
        print("SI")
    print()

    ##############################################Ejercicio 3##################################################
    print("Ejercicio 3")
    resolver_problemas_de_fisica("practica0_ejercicio3_entrada.txt")
    print()

main()