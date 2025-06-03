import sqlite3
import os
from cadastro import Cadastro
from cadastro import Cadastro_adm
from datetime import datetime


class BancoDeDados:
    def __init__(self, nome_banco="banco.sqlite"):
        # Garante que o banco seja criado no mesmo diretório do script bd.py
        self.nome_banco = os.path.join(os.path.dirname(__file__), nome_banco)
        self.conn = None

    def conectar(self):
        try:
            self.conn = sqlite3.connect(self.nome_banco)
            # Garante que as tabelas existam com o schema correto ao conectar
            self._verificar_e_criar_tabelas()
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def _verificar_e_criar_tabelas(self):
        """Verifica e cria as tabelas se não existirem (chamado internamente)."""
        self.criar_tabela_pessoa()
        self.criar_tabela_adm()
        # A criação/migração do log é tratada separadamente ou no script de migração
        # Mas garantimos que a tabela exista com o schema correto aqui também
        self.criar_tabela_log()

    def criar_tabela_pessoa(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS Pessoa(
                    cpf TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    login TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL,
                    bloco INTEGER,
                    numero_ap INTEGER,
                    email TEXT NOT NULL UNIQUE,
                    data_cadastro TEXT
                    )"""
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criar/verificar tabela Pessoa: {e}")

    def criar_tabela_adm(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS Adm(
                    cpf TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    login TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL,
                    data_cadastro TEXT
                    )"""
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criar/verificar tabela Adm: {e}")

    def criar_tabela_log(self):
        """Cria a tabela Log com o schema correto se não existir."""
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS Log(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_modificador TEXT NOT NULL,
                    acao TEXT NOT NULL,
                    data_hora TEXT,
                    cpf_modificado TEXT,
                    cpf_modificador TEXT
                    )"""
                )
                # Verifica se as colunas existem, se não, tenta adicioná-las (migração simples)
                cursor.execute("PRAGMA table_info(Log)")
                columns = [col[1] for col in cursor.fetchall()]
                if "nome_modificador" not in columns:
                    print("Adicionando coluna 'nome_modificador' à tabela Log...")
                    cursor.execute("ALTER TABLE Log ADD COLUMN nome_modificador TEXT DEFAULT 'N/A' NOT NULL")
                if "cpf_modificado" not in columns:
                    print("Adicionando coluna 'cpf_modificado' à tabela Log...")
                    cursor.execute("ALTER TABLE Log ADD COLUMN cpf_modificado TEXT")
                if "cpf_modificador" not in columns:
                    print("Adicionando coluna 'cpf_modificador' à tabela Log...")
                    cursor.execute("ALTER TABLE Log ADD COLUMN cpf_modificador TEXT")

                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criar/verificar tabela Log: {e}")

    def buscar_nome_por_cpf(self, cpf):
        """Busca o nome de um usuário (Pessoa ou Adm) pelo CPF."""
        if not self.conn or not cpf:
            return "Desconhecido"
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT nome FROM Pessoa WHERE cpf = ?", (cpf,))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]
            cursor.execute("SELECT nome FROM Adm WHERE cpf = ?", (cpf,))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]
            # print(f"WARN: CPF {cpf} não encontrado em Pessoa ou Adm.")
            return f"CPF {cpf} não encontrado"
        except sqlite3.Error as e:
            print(f"Erro ao buscar nome por CPF ({cpf}): {e}")
            return "Erro na busca"

    def inserir_log(self, acao, cpf_modificado, cpf_modificador):
        """Insere um registro na tabela Log."""
        if self.conn:
            try:
                nome_modificador = self.buscar_nome_por_cpf(cpf_modificador)
                data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO Log (nome_modificador, acao, data_hora, cpf_modificado, cpf_modificador) VALUES (?, ?, ?, ?, ?)",
                    (nome_modificador, acao, data_hora, cpf_modificado, cpf_modificador)
                )
                self.conn.commit()
                log_id = cursor.lastrowid
                # print(f"Log inserido com sucesso! ID: {log_id}")
                return log_id
            except sqlite3.Error as e:
                # Verifica se o erro é sobre a coluna inexistente e tenta criar
                if "no such column" in str(e):
                    print(f"Erro de coluna no Log: {e}. Tentando recriar/ajustar tabela Log...")
                    self.criar_tabela_log() # Tenta corrigir o schema
                    # Tenta inserir novamente após correção
                    try:
                        cursor.execute(
                            "INSERT INTO Log (nome_modificador, acao, data_hora, cpf_modificado, cpf_modificador) VALUES (?, ?, ?, ?, ?)",
                            (nome_modificador, acao, data_hora, cpf_modificado, cpf_modificador)
                        )
                        self.conn.commit()
                        log_id = cursor.lastrowid
                        print(f"Log inserido com sucesso após recriação da tabela! ID: {log_id}")
                        return log_id
                    except sqlite3.Error as e2:
                        print(f"Erro ao inserir log mesmo após tentativa de correção: {e2}")
                        return None
                else:
                    print(f"Erro ao inserir log: {e}")
                    return None
        return None

    # --- Funções Pessoa --- #
    def inserir_pessoa(self, pessoa: Cadastro, cpf_modificador):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO Pessoa (cpf, nome, login, senha, bloco, numero_ap, email, data_cadastro) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (pessoa.cpf, pessoa.nome, pessoa.login, pessoa.get_senha(), pessoa.bloco, pessoa.numero_ap,
                     pessoa.email, pessoa.data_cadastro)
                )
                self.conn.commit()
                print("Pessoa inserida com sucesso!")
                self.inserir_log("Cadastro de novo usuário", pessoa.cpf, cpf_modificador)
            except sqlite3.IntegrityError as e:
                 if "UNIQUE constraint failed: Pessoa.cpf" in str(e):
                     raise ValueError(f"CPF {pessoa.cpf} já cadastrado.")
                 elif "UNIQUE constraint failed: Pessoa.login" in str(e):
                     raise ValueError(f"Login '{pessoa.login}' já cadastrado.")
                 elif "UNIQUE constraint failed: Pessoa.email" in str(e):
                     raise ValueError(f"Email '{pessoa.email}' já cadastrado.")
                 else:
                     print(f"Erro de integridade ao inserir pessoa: {e}")
                     raise e
            except sqlite3.Error as e:
                print(f"Erro ao inserir pessoa: {e}")
                raise e

    def atualizar_pessoa(self, cpf_modificado, cpf_modificador, novo_nome=None, novo_email=None, novo_login=None, novo_senha=None,
                         novo_bloco=None, novo_numero_ap=None):
        if self.conn:
            campos_atualizados = []
            valores = []
            query = "UPDATE Pessoa SET "

            if novo_nome is not None: campos_atualizados.append("nome = ?"); valores.append(novo_nome)
            if novo_email is not None: campos_atualizados.append("email = ?"); valores.append(novo_email)
            if novo_login is not None: campos_atualizados.append("login = ?"); valores.append(novo_login)
            if novo_senha is not None: campos_atualizados.append("senha = ?"); valores.append(novo_senha)
            if novo_bloco is not None: campos_atualizados.append("bloco = ?"); valores.append(novo_bloco)
            if novo_numero_ap is not None: campos_atualizados.append("numero_ap = ?"); valores.append(novo_numero_ap)

            if not campos_atualizados: return # Nada a fazer

            query += ", ".join(campos_atualizados)
            query += " WHERE cpf = ?"
            valores.append(cpf_modificado)

            try:
                cursor = self.conn.cursor()
                cursor.execute(query, tuple(valores))
                rows_affected = cursor.rowcount
                self.conn.commit()
                if rows_affected > 0:
                    print(f"Pessoa (CPF: {cpf_modificado}) atualizada com sucesso!")
                    self.inserir_log("Usuário atualizado", cpf_modificado, cpf_modificador)
                else:
                    print(f"Nenhuma pessoa encontrada com o CPF {cpf_modificado} para atualizar.")
            except sqlite3.IntegrityError as e:
                 if "UNIQUE constraint failed: Pessoa.login" in str(e):
                     raise ValueError(f"Login '{novo_login}' já está em uso.")
                 elif "UNIQUE constraint failed: Pessoa.email" in str(e):
                     raise ValueError(f"Email '{novo_email}' já está em uso.")
                 else:
                     print(f"Erro de integridade ao atualizar pessoa: {e}")
                     raise e
            except sqlite3.Error as e:
                print(f"Erro ao atualizar pessoa: {e}")
                raise e

    def deletar_pessoa(self, cpf_modificado, cpf_modificador):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT nome FROM Pessoa WHERE cpf = ?", (cpf_modificado,))
                pessoa = cursor.fetchone()
                if pessoa:
                    cursor.execute("DELETE FROM Pessoa WHERE cpf = ?", (cpf_modificado,))
                    self.conn.commit()
                    print(f"Pessoa (CPF: {cpf_modificado}) deletada com sucesso!")
                    self.inserir_log("Usuário excluído", cpf_modificado, cpf_modificador)
                    return True
                else:
                    print(f"Nenhuma pessoa encontrada com o CPF {cpf_modificado} para deletar.")
                    return False
            except sqlite3.Error as e:
                print(f"Erro ao deletar pessoa: {e}")
                raise e
        return False

    def listar_pessoas(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT cpf, nome, login, bloco, numero_ap, email, data_cadastro FROM Pessoa")
                return cursor.fetchall()
            except sqlite3.Error as e:
                print(f"Erro ao listar pessoas: {e}")
                return []
        return []

    def buscar_pessoa_por_cpf(self, cpf):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT cpf, nome, login, senha, bloco, numero_ap, email, data_cadastro FROM Pessoa WHERE cpf = ?", (cpf,))
                return cursor.fetchone()
            except sqlite3.Error as e:
                print(f"Erro ao buscar pessoa por CPF: {e}")
                return None
        return None

    # --- Funções Adm --- #
    def inserir_adm(self, adm: Cadastro_adm, cpf_modificador):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO Adm (cpf, nome, login, senha, data_cadastro) VALUES (?, ?, ?, ?, ?)",
                    (adm.cpf, adm.nome, adm.login, adm.get_senha(), adm.data_cadastro)
                )
                self.conn.commit()
                print("Administrador inserido com sucesso!")
                self.inserir_log("Cadastro de novo ADM", adm.cpf, cpf_modificador)
            except sqlite3.IntegrityError as e:
                 if "UNIQUE constraint failed: Adm.cpf" in str(e):
                     raise ValueError(f"CPF {adm.cpf} já cadastrado como ADM.")
                 elif "UNIQUE constraint failed: Adm.login" in str(e):
                     raise ValueError(f"Login '{adm.login}' já cadastrado como ADM.")
                 else:
                     print(f"Erro de integridade ao inserir ADM: {e}")
                     raise e
            except sqlite3.Error as e:
                print(f"Erro ao inserir adm: {e}")
                raise e

    def deletar_adm(self, cpf_modificado, cpf_modificador):
        """Deleta um administrador e registra o log."""
        if self.conn:
            # Impedir que o ADM se auto-delete
            if cpf_modificado == cpf_modificador:
                print("Erro: Um administrador não pode excluir a própria conta.")
                raise ValueError("Um administrador não pode excluir a própria conta.")

            try:
                cursor = self.conn.cursor()
                # Verifica se o ADM existe
                cursor.execute("SELECT nome FROM Adm WHERE cpf = ?", (cpf_modificado,))
                adm = cursor.fetchone()

                if adm:
                    cursor.execute("DELETE FROM Adm WHERE cpf = ?", (cpf_modificado,))
                    self.conn.commit()
                    print(f"Administrador (CPF: {cpf_modificado}) deletado com sucesso!")
                    # Registra o log da deleção do ADM
                    self.inserir_log("Administrador excluído", cpf_modificado, cpf_modificador)
                    return True
                else:
                    print(f"Nenhum administrador encontrado com o CPF {cpf_modificado} para deletar.")
                    return False
            except sqlite3.Error as e:
                print(f"Erro ao deletar administrador: {e}")
                raise e
        return False

    def listar_adms(self):
        """Lista todos os administradores cadastrados."""
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT cpf, nome, login, data_cadastro FROM Adm")
                return cursor.fetchall()
            except sqlite3.Error as e:
                print(f"Erro ao listar administradores: {e}")
                return []
        return []

    # --- Função de Login --- #
    def validar_login(self, login, senha):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                # Verifica Adm primeiro
                cursor.execute("SELECT cpf, nome FROM Adm WHERE login = ? AND senha = ?", (login, senha))
                adm = cursor.fetchone()
                if adm:
                    # print("Login de administrador bem-sucedido!")
                    return ("Adm", adm[0], adm[1]) # Retorna tipo, cpf, nome

                # Verifica Pessoa
                cursor.execute("SELECT cpf, nome FROM Pessoa WHERE login = ? AND senha = ?", (login, senha))
                pessoa = cursor.fetchone()
                if pessoa:
                    # print("Login de usuário bem-sucedido!")
                    return ("Pessoa", pessoa[0], pessoa[1]) # Retorna tipo, cpf, nome

                # print("Login ou senha inválidos.")
                return None
            except sqlite3.Error as e:
                print(f"Erro ao validar login: {e}")
                return None
        return None

    def fechar_conexao(self):
        if self.conn:
            self.conn.close()
            print("Conexão com o banco de dados fechada.")

# Exemplo de uso (opcional, para teste)
if __name__ == '__main__':
    print("Executando testes básicos do bd.py...")
    bd_teste = BancoDeDados("teste_banco.sqlite") # Usa um banco de teste
    # Limpa o banco de teste se existir
    if os.path.exists(bd_teste.nome_banco):
        os.remove(bd_teste.nome_banco)
        print("Banco de teste anterior removido.")

    bd_teste.conectar()

    # Adiciona um ADM inicial para testes
    try:
        adm_inicial = Cadastro_adm('00000000000', 'admin_root', 'Admin Root', 'root123', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        bd_teste.inserir_adm(adm_inicial, '00000000000') # Auto-cadastro inicial
    except ValueError as e:
        print(f"Erro ao inserir ADM inicial: {e}")

    # Adiciona um ADM para ser deletado
    try:
        adm_deletar = Cadastro_adm('11111111111', 'adm_del', 'Adm A Deletar', 'del123', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        bd_teste.inserir_adm(adm_deletar, '00000000000')
    except ValueError as e:
        print(f"Erro ao inserir ADM para deletar: {e}")

    print("\nListando ADMs antes da deleção:")
    adms = bd_teste.listar_adms()
    for adm in adms:
        print(adm)

    print("\nTentando deletar ADM '11111111111' pelo ADM '00000000000':")
    try:
        bd_teste.deletar_adm(cpf_modificado='11111111111', cpf_modificador='00000000000')
    except Exception as e:
        print(f"Erro ao deletar ADM: {e}")

    print("\nTentando deletar ADM '00000000000' por ele mesmo (deve falhar):")
    try:
        bd_teste.deletar_adm(cpf_modificado='00000000000', cpf_modificador='00000000000')
    except ValueError as e:
        print(f"Falha esperada ao tentar auto-deleção: {e}")
    except Exception as e:
        print(f"Erro inesperado ao tentar auto-deleção: {e}")

    print("\nListando ADMs após a deleção:")
    adms = bd_teste.listar_adms()
    for adm in adms:
        print(adm)

    bd_teste.fechar_conexao()
    # Limpa o banco de teste
    # if os.path.exists(bd_teste.nome_banco):
    #     os.remove(bd_teste.nome_banco)
    #     print("Banco de teste removido.")
    print("Testes básicos concluídos.")

