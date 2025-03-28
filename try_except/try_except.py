try:
    f = open('nomes.tex')
    s = f.readline()
    i = int(s.strip())
except FileNotFoundError:
    print("não existe arquivo")
except IOError:
    print("erro na abertura do arquivo")
except ValueError:
    print("erro no valor ")
except Exception as e:
    print("erro inesperado:{e}")
    raise
    
