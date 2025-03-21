from conda.env.env import print_result

texto = "eu quero comprar algo depois com meus 1.50"

print(f'começa em 0 e vai até o numero 20 e pula de 2 em 2:{texto[0:20:2]}')

print(f'tamanho: {len(texto)}')

print(f'quantas letras A tem: {texto.count('a')}')

print(f'quantos "A" tem entre a posição 5 e 30:{texto.count('a',5,30)}')

print(f'{texto.find("Eu")}')

print(f'{texto.find('pudim')}')

print(f'retorna false pois não tem{'string' in texto}')

print(f'retorna true pois tem no texto{'depois'}')

novo_texto = texto.replace("vou comprar algo depois com meu dinheiro")
print(novo_texto)

print(texto.startswith("vou"))
print(texto.startswith("eu"))

print(texto.endswith("dinheiro"))
print(texto.endswith("1.50"))

print(texto.lower())
print(texto.upper())
print(texto.capitalize())
print(texto.title())
print(texto.swapcase())


nome = str(input("digite seu nome:"))
print(f'ola, {nome}!')
print(f'ola, {nome.strip()}!')

print(nome.rstrip())

print(nome.lstrip())

texto = 'bom dia '
texto.split()
print(texto)

