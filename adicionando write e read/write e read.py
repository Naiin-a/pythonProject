arquivo = open ('C:/Users/leafa/PycharmProjects/PythonProject1/aaa.txt')
arquivo.write("rafael")
arquivo.close()

arquivo = open ('C:/Users/leafa/PycharmProjects/PythonProject1/aaa.txt')
print(arquivo.readline())
arquivo.close()

caminho_arquivo = 'C:/Users/leafa/PycharmProjects/PythonProject1/aaa.txt'

arquivo = open(caminho_arquivo)

linha1 = arquivo.readline()
print(f'linha 1:{linha1}')
linha2 = arquivo.readline()
print(f'linha 2:{linha2}')

arquivo.close()
