from dataclasses import dataclass
from pessoa import Pessoa
from marca import  Marca

@dataclass
class Veiculo:
    placa: str
    cor: str
    propietario: Pessoa
    marca: Marca
    
