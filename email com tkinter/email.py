import smtplib
from email.mime.text import MIMEText
from tkinter import Tk, Label, Entry, Button, StringVar, Text, messagebox


def enviar_email():
    remetente = remetente_var.get()
    destinatario = destinatario_var.get()
    assunto = assunto_var.get()
    corpo = corpo_var.get("1.0", "end-1c")


    msg = MIMEText(corpo)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    try:
        # Envia o email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(remetente, 'umes vjro oeho dmwm')
            server.sendmail(remetente, destinatario, msg.as_string())
            messagebox.showinfo("Sucesso", "Email enviado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível enviar o email: {e}")



root = Tk()
root.title("Enviar Email")


remetente_var = StringVar()
destinatario_var = StringVar()
assunto_var = StringVar()


Label(root, text="Email do Remetente:").pack()
Entry(root, textvariable=remetente_var).pack()

Label(root, text="Email do Destinatário:").pack()
Entry(root, textvariable=destinatario_var).pack()

Label(root, text="Assunto:").pack()
Entry(root, textvariable=assunto_var).pack()

Label(root, text="Corpo da Mensagem:").pack()
corpo_var = Text(root, height=10, width=30)
corpo_var.pack()


Button(root, text="Enviar Email", command=enviar_email).pack()


root.mainloop()
