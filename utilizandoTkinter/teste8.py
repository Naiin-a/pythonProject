import tkinter as tk

janela = tk.Tk()

frame1 = tk.Frame(master=janela, width=100, height=100, bg="red")
frame1.pack(fill=tk.X)
frame2 = tk.Frame(master=janela, width=50, height=50, bg="green")
frame2.pack(fill=tk.X)
frame3 = tk.Frame(master=janela, width=25, height=25, bg="blue")
frame3.pack(fill=tk.X)
janela.mainloop()
