import sqlite3

class Marca:
    id: int
    nome: str
    sigla: str

    def inserir_marca(self, marca: Marca):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO Marca VALUES (?, ?, ?)",
                (
                    marca.id,
                    marca.nome,
                    marca.sigla
                ),
            )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao inserir Marca {e}")

    def atualizar_marca(self, marca):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "UPDATE Marca marca_id =?, marca_nome =? WHERE marca.sigla =?"
                )
            except sqlite3.Error as e:
                print(f"Erro ao atualizar marca: {e}")

    def apagar_marca(self, marca):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM Marca WHERE marca.id=?",(marca.id,))
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao apagar marca: {e}")

    def buscar_todas_marcas(self):
        marcas = []
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM Marca")
                for row in cursor.fetchall():
                    id, nome, sigla =  row
                    marcas.append(Marca(id, nome, sigla))
            except sqlite3.Error as e:
                print(f"Error ao buscar marcas: {e}")
        return marcas
