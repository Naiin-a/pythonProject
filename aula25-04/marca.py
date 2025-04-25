from dataclasses import dataclass
from datetime import date

@dateclass
class Pessoa:
    cpf: int
    nome: str
    nascimento: date
    oculos: bool
    
