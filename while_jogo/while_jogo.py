import random
numero_secreto = random.randint(1,100)
tentativas = 0

while True:
    x=int(input("digite um numero:"))
    tentativas =tentativas+1

    if x == numero_secreto:
        print("acentou")
        break
    elif tentativas == 3:
        print("perdeu")
        break

    elif x > numero_secreto:
        print("tente um numero menor")
    elif x < numero_secreto:
        print("tente um numero maior")
