caminho_arquivo = 'C:/Users/leafa/PycharmProjects/PythonProject1/aaa.txt'

arquivo = open("aaa.txt")
arquivo.write("rafael")
arquivo.writelines(["\nrafael", "\nataga", "\ndiogo"])
arquivo.close()

arquivo = open(caminho_arquivo, 'r')
linhas = arquivo.readline()

for i, linha in enumerate(linhas, start = 1):
    print(f"linha{i}:{linha}")
    
