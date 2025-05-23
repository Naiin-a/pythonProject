import  tkinter as tk
import random

def janela_divertida():
    cores = ['red','blue', 'green', 'purple', 'orange', 'pink']
    segunda_janela = tk.Tk()
    segunda_janela.title('Sobre')
    segunda_janela.geometry("300x200")

    texto = tk.Label(segunda_janela, text="Janela Sobre!", font=("Comic Sans MS", 14))
    texto.pack(pady=20)

    def mudar_cor():
        cor_aleatoria = random.choice(cores)
        segunda_janela.configure(bg = cor_aleatoria)

    botao_cor = tk.Button(segunda_janela, text='Mudar Cor', command=mudar_cor)
    botao_cor.pack(pady=10)

    segunda_janela.mainloop()

if __name__ == "__main__":
    janela_divertida()