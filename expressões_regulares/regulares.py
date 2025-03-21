import re

texto = 'meu email é exemplo@email.com, entre em contato'
padrao = r'\b\w+@\w+\.\w+\b' #padrão para econtrar endereços

novo_texto = re.sub(padrao,'[email oculto]', texto)
print(novo_texto)
