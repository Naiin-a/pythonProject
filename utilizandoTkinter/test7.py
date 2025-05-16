import tkinter as tk

def ao_focar(event):
     if entrada.get() == "digite o seu nome aqui":
         entrada.delete(0,"end")
         entrada.config(fg="pink")


def ao_desfocar(event):
    if not entrada.get():
        entrada.insert(0,"digite o seu nome aqui: ")
        entrada.config(fg="black")

janela = tk.Tk()

entrada = tk.Entry(width=40, bg="white",fg="black")
entrada.pack()
entrada.insert(0,"digite seu nome")

entrada.bind("<FocusIn>", ao_focar)
#quando o caixa de entrada ghanha o focom chame a função ao_focar

entrada.bind("<FocusOut>", ao_desfocar)
#quando a caixa de entrada perde o foco, chame a função  ao_desfocar

janela.mainloop()

