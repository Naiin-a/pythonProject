import tkinter as tk

class Exemplo_grid:
    def __init__(self):
        self.janela = tk.Tk()
        for i in range(3):
            self.janela.columnconfigure(i, weight =1, minsize=75)
            self.janela.rowconfigure(i, weight=1, minsize=50)
            for j in range(3):
                frame = tk.Frame(master=self.janela, relief= tk.RAISED, borderwidth=1)
                frame.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                label = tk.Label(master=frame, text=f"linha {i}\nColuna {j}")
                label.pack()
        self.janela.mainloop()

if __name__ == "__main__":
    Exemplo_grid()

janela = tk.Tk()
janela.columnconfigure(0, minsize=250)
janela.rowconfigure([0,1], minsize=100)

label1 = tk.Label(text="A")
label1.grid(row=0, column=0, sticky = "ne")

label2 = tk.Label(text="B")
label2.grid(row=1, column=0, sticky="sw")

janela.mainloop()
