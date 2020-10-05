import re

# Ejercicio 1
p = re.compile('([0-9]{1,3}\.){3}[0-9]{1,3}$')
if p.match('84.125.78.125'):
    print("SI ES UN IP")
else:
    print("NO ES UN IP")


#Ejercicio 2
p = re.compile('[a-zA-Z][a-zA-Z0-9]*')
if p.match('varNum1'):
    print("SI ES UNA VARIABLE")
else:
    print("NO ES UN VARIABLE")