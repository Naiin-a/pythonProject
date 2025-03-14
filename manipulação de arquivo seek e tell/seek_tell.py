caminho_arquivo = 'C:/Users/leafa/PycharmProjects/PythonProject1/aaa.txt'

with open (caminho_arquivo, 'w') as arquivo:
    arquivo.write('esta é minha linha\n')
    arquivo.write('estaé a segunda linha\n')

    linhas = ['esta é a primeira linha em uma lista\n','esta é a segunda linha']

    with open("exemplo", 'w',encoding = "utf-8") as f:
        f.write("exemeplo de uso dos metodos seek( e tell( em python")

    with open("exemplo", 'r',encoding= "utf-8") as f:
        print("posição inicial do cursor",f.tell())

        conteudo = f.read(10)
        print("conteudo lida:",conteudo)
        print("posição do cursor apos ler 10 caracteres:",f.tell())

        f.seek(15,0)
        print("posição do cursos apos seek(0, 0):", f.tell())
        
