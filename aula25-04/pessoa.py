import sqlite3

class Pessoa:
    cpf: str
    nome: str
    nascimento: date
    oculos: bool

    def inserir_pessoa(self, pessoa: Pessoa):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO Pessoa VALUES (?, ?, ?, ?)",
            (
                pessoa.cpf,
                pessoa.nome,
                pessoa.nascimento,
                pessoa.oculos
            ),)
                self.conn.commit()
            except sqlite3.Error as e:
                    print(f"Erro ao inserir pessoa: {e}")

    def atualizar_pessoa(self, pessoa):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "UPDATE Pessoa SET nome=?, nascimento=?, oculos=? WHERE cpf=?",
                    (pessoa.nome, pessoa.nascimento, pessoa.oculos, pessoa.cpf),
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao atualizar pessoa: {e}")

    def apagar_pessoa(self, pessoa):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM Pessoa WHERE nome=?", (pessoa.nome,))
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao apagar o nome : {e}")

    def buscar_todas_pessoas(self):
        pessoas = []
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM Pessoa")
                for row in cursor.fetchall():
                    cpf, nome, nascimento, oculos =  row
                    pessoas.append(Pessoa(cpf, nome, nascimento, oculos))
            except sqlite3.Error as e:
                print(f"Error ao buscar pessoas: {e}")
        return pessoas

    def buscar_pessoa_por_cpf(self, cpf: str):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM Pessoa WHERE cpf=?", (cpf,))
                row = cursor.fetchone()
                if row:
                    cpf, nome, nascimento, oculos = row
                    return Pessoa(cpf, nome, nascimento, oculos)
            except sqlite3.Error as e:
                print(f"Erro ao buscar pessoa por CPF: {e}")
        return None

    def fechar_conexao(self):
        if self.conn:
            self.conn.close()
            self.conn = None
