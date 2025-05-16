import tkinter as tk
from tkinter import ttk

class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.title("Exemplo 00")
        self.pack(padx=10, pady=10)
        ttk.Label(self, text="Digite algo:").pack()
        self.entrada = ttk.Entry(self)
        self.entrada.pack()
        ttk.Button(self, text="Mostrar", command=self.exibir).pack()

    def exibir(self):
        print("Entrada:", self.entrada.get())

root = tk.Tk()
App(root)
root.mainloop()

