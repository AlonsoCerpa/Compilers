import re

p = re.compile('[0-9]+$')

if p.match('amigo'):
    print("SI ES UN NUMERO")
else:
    print("NO ES UN NUMERO")
    



regstr = '[a-z]+'
text = 'abc cde 777ghi jkl999mno'
groups = re.findall(regstr, text)

for group in groups:
    print(group)
