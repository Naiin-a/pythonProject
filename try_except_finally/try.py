def divide(x, y):
    try:
        resultado = x/y
    except ZeroDivisionError:
        print("erro no calculo")
    else:
        print("certa a divisão")
    finally:
        print("sempre sera imprimido")
        
divide(4,2)
divide(2,0)
