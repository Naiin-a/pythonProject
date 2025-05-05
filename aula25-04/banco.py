import os
import sqlite3
from pessoa import Pessoa
from marca import Marca
from veiculo import Veiculo

class BancoDeDados:
    def __init__(self, nome_banco="banco.sqlite"):
        self.nome_banco = os.path.join(os.path.dirname(__file__), nome_banco)
        self.conn = None

    def conectar(self):
        try:
            self.conn = sqlite3.connect(self.nome_banco)
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def criar_tabelas(self):
        self.criar_tabela_pessoa()
        self.criar_tabela_marca()
        self.criar_tabela_veiculo()


    def criar_tabela_pessoa(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS Pessoa(
                    cpf INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL,
                    nascimento DATE,
                    oculos BOOLEAN
                    )"""
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criar tabela Pessoa: {e}")


    def criar_tabela_marca(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS Marca (
                            id INTEGER PRIMARY KEY,
                            nome TEXT NOT NULL,
                            sigla TEXT
                            )"""
                )
            except sqlite3.Error as e:
                print(f"Erro ao criar tabela Marca: {e}")


    def criar_tabela_veiculo(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS Veiculo (
                placa TEXT PRIMARY KEY,
                cor TEXT NOT NULL,
                cpf_proprietario INTEGER,
                id_marca INTEGER,
                FOREIGN KEY(cpf_proprietario) REFERENCES Pessoa(cpf),
                FOREIGN KEY(id_marca) REFERENCES Marca(id))"""
                )
                self.conn.commit()

            except sqlite3.Error as e:
                print(f"Erro ao criar tabela Veiculo: {e}")

            except sqlite3.DatabaseError as e:
                print(f"Erros genericos: {e}")

            except sqlite3.IntegrityError as e:
                print(f"Violação de restrições: {e}")

            except sqlite3.OperationalError as e:
                print(f"Erros operacionais: {e}")

            except sqlite3.ProgrammingError as e:
                print(f"Uso incorreto da API SQLite: {e}")

            except sqlite3.DataError as e:
                print(f"Dados incorretos: {e}")
