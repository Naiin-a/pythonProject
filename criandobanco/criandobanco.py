from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///:memory", echo=True)

Base = declarative_base()

class Usuario(Base):

    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key = True)
    nome = Column(String)
    idade = Column(Integer)

    def __repr__(self):
        return f" usuarios id={self.id}, nome={self.nome}, idade={self.idade})"

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

usuario1 = Usuario(nome= 'Rafael', idade = 19)
usuario2 = Usuario(nome = 'duda', idade= 299)

session.add(usuario1)
session.add(usuario2)

session.commit()

usuarios = session.query(Usuario).all()
for usuario in usuarios:
    print(usuario)

