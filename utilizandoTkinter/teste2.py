import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("interface")
style = ttk.Style()
style.theme_use("clam") # ou 'alt' 'defaut', 'vista'
style.configure("Tbutton",font=("Segoe UI",10),padding=10)

ttk.Label(root,text="Nome:",font=("Segoe UI",10)).pack(pady=5)
ttk.Entry(root).pack(pady=5)
ttk.Button(root, text="Enviar").pack(pady=10)

root.mainloop()