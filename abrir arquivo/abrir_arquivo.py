arquivo = open ('C:/Users/leafa/PycharmProjects/PythonProject1/aaa.txt')

print('nome do arquivo', arquivo.name)
print('tamanho do arquivo:',arquivo.tell())
print('modo do arquivo:',arquivo.mode)
print('arquivo esta fechado?', arquivo.closed)

arquivo.close()

print('arquivo esta fechado?', arquivo.closed)
