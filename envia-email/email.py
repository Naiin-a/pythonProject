import smtplib

email = input('Sender email: ')
receiver_email = input("Receiver email: ")

subject = input("subject: ")
message = input("mensage: ")

text = f"subject:{subject}\n\n{message}"

server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()

server.login(email,"Sua chave do google password")

server.sendmail(email, receiver_email,text)

print("email foi enviado para" + receiver_email)
