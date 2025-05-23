import tkinter as tk
from tkinter import ttk

class TreeviewExempleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("exemplo de treeview")

        self.tree = ttk.Treeview(
            root, columns=("nome","idade", "profissão"), show="headings"
        )

        self.tree.heading("nome",text="Nome")
        self.tree.heading("idade", text="idade")
        self.tree.heading("profissão", text="profissão")

        self.tree.column("Nome", width=150)
        self.tree.column("Idade", width=80)
        self.tree.column("Profissão", width=150)

        self.tree.insert("","end",values=("rafael",50,"dev"))
        self.tree.insert("", "end", values=("paulo", 90, "pedreiro"))
        self.tree.insert("", "end", values=("maria", 2, "pai de pet"))

        self.tree.pack(pady=20)


        self.btn_add_row = tk.Button(
            root, text="adicionar linha", command=self.adicionar_linha
        )
        self.btn_add_row.pack(pady=10)

    def adicionar_linha(self):
        self.tree.insert("","end", values=("Gilson", 68, "Contador"))

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeviewExempleApp(root)
    root.mainloop()



