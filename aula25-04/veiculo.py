import sqlite3


class Veiculo:
    placa: str
    cor: str
    proprietario: Pessoa
    marca: Marca

    def inserir_veiculo(self, veiculo: Veiculo):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO Veiculo VALUES (?, ?, ?, ?)",
                    (
                        veiculo.placa,
                        veiculo.cor,
                        veiculo.proprietario.cpf,
                        veiculo.marca.id,
                    ),
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao inserir veículo: {e}")

    def atualizar_veiculo(self, veiculo):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "UPDATE Veiculo SET cor=?, cpf_proprietario=?, id_marca=? WHERE placa=?",
                    (
                        veiculo.cor,
                        veiculo.proprietario,
                        veiculo.marca.id,
                        veiculo.placa
                    ),
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao atualizar veiculo: {e}")

    def apagar_veiculo(self, veiculo):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM Veiculo WHERE placa=?", (veiculo.placa,))
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao apagar veiculo: {e}")


    def buscar_todos_veiculos(self):
        veiculos = []
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM Veiculo")
                for row in cursor.fetchall():
                    placa, cor, cpf_proprietario, id_marca =  row
                    proprietario = self.buscar_pessoa_por_cpf(cpf_proprietario)
                    marca = self.buscar_marca_por_id(id_marca)
                    veiculos.append(Veiculo(placa, cor, proprietario, marca))
            except sqlite3.Error as e:
                print(f"Error ao buscar veiculos: {e}")
        return veiculos
