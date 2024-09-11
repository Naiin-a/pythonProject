def soma(a, b):
    return a + b

def subtracao(a, b):
    return a - b

def multiplicacao(a, b):
    return a * b

def divisao(a, b):
    if b == 0:
        retunr"divisao por zero nao permitida"
    return a / b

def calculadora():

    repeticoes = int(input("digite o numero de repetiçoes:"))

    for i in range(repeticoes):

        a = float(input(f"interacao{i+1} - digite o valor de A:"))
        b = float(input(f"interacao{i+1} - digite o valor de B:"))

        print(f"soma:{soma(a, b)}")
        print(f"subtracao:{subtracao(a, b)}")
        print(f"multiplicacao:{multiplicacao(a, b)}")
        print(f"divisao:{divisao(a, b)}")
        print('-'*30)


calculadora()
