from fatatime import date
from pessoa import Pessoa
from marca import Marca
from veiculo import Veiculo

pessoa = Pessoa(cpf=12345678910, nome="Rafael", nascimento=date(2005,9,11),oculos=True)

marca1 = Marca(id=1, nome="hb20",sigla="pila")

veiculo = Veiculo(placa="hw23j4", cor="vermelho", propietario=pessoa, marca=marca1)

