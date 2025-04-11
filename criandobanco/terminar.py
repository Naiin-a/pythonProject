from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db = dataset.connect('sqlite:///:memory:')

class criar:
    __tablename__ = 'pessoa'
    nome =Column(String)
    telefone = Column(Integer)
    cpf = Column(Integer,primary_key = true)

usuario1 = pessoa(nome = rafael, telefone= 100000, cpf= 12312312)
usuario2 = pessoa(nome = paulo, telefone =  12312312, cpf = 1231231)

table.delete()

for pessoa in table:
    print(usuario1)

john = table.find_one(name='John Doe')

