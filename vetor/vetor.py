a = int
while True:
    if (a == 0):
        print("saindo")
        break
    nome = ["nome","n1","n2"]
    media = ['nome', 'media']
    nome[0] = str(input("digite o nome do aluno:"))
    nome[1] = float(input("digite a primeira nota:"))
    nome[2] = float(input("digite a segunda nota:"))
    float(nome[1])
    float(nome[2])
    media[1] = (nome[1] + nome[2]) / 2
    float(media[1])
    media[0] = nome[0]
    print(f"a media do aluno {media[0]} foi media{media[1]}:")
    a = int(input("se deseja parar digitre 0:"))
