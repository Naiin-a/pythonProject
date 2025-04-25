import os
import sqlite3
from pessoa import Pessoa
from marca import  Marca
from veiculo import Veiculo

class BancoDeDados:
    def __init__(self, nome_banco="banco,sqlite"):
        self.nome_banco = os.path.join(os,path.dirname(__file__),nome_banco)
        self.conn = None
    
    def conectar(self):
        try:
            self.conn = sqlite3.connect(self.nome_banco)
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            
            
    
    def criar_tabelas(selfself):
        self.criar_tabela_pessoa()
        self.criar_tabela_marca()
        self.crar_tabela_veiculo()
    
    def criar_tabela_pessoa(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS PESSOA (
                        cpf INTEGER PRIMARY KEY,
                        nome TEXT NOT NULL,
                        nascimento DATE,
                        oculos BOOLEAN
                        )"""
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criar tabela pessoa: {e}")

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
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criar tabela marca: {e}")

    def criar_tabela_veiculo(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS Veiculo(
                        placa INTEGER PRIMARY KEY,
                        cor TEXT NOT NULL,
                        cpf_proprietario INTEGER,
                        id_marca INTEGER,
                        FOREIGN KEY(cpf_proprietario) REFERENCES pessoa(cpf),
                        FOREIGN KEY(id_marca) REFERENCES marca(id)
                        )"""
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criar tabela veiculo: {e}")
            except sqlite3.IntegrityError as e:
                print(f"erro de integridade{e}")
            except sqlite3.OperationalError as e:
                print(f"erro de operacionais{e}")
