#!/usr/bin/env python3.11
import sqlite3
import os
from datetime import datetime

# Define o caminho para o banco de dados na mesma pasta do script
DB_PATH = os.path.join(os.path.dirname(__file__), "banco.sqlite")

def buscar_nome_por_cpf(conn, cpf):
    """Busca o nome de um usuário (Pessoa ou Adm) pelo CPF dentro da mesma conexão."""
    if not conn or not cpf:
        return "Desconhecido"
    try:
        cursor = conn.cursor()
        # Tenta buscar na tabela Pessoa
        cursor.execute("SELECT nome FROM Pessoa WHERE cpf = ?", (cpf,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        # Se não encontrar, tenta buscar na tabela Adm
        cursor.execute("SELECT nome FROM Adm WHERE cpf = ?", (cpf,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        print(f"WARN: CPF {cpf} não encontrado em Pessoa ou Adm.")
        return f"CPF {cpf} não encontrado"
    except sqlite3.Error as e:
        print(f"Erro ao buscar nome por CPF ({cpf}): {e}")
        return "Erro na busca"

def migrate_log_schema():
    conn = None
    try:
        print(f"Conectando ao banco de dados: {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("Verificando schema atual da tabela Log...")
        cursor.execute("PRAGMA table_info(Log)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"Colunas encontradas: {columns}")

        # Verifica se a migração já foi feita ou se a tabela tem o schema novo
        if "nome_modificador" in columns and "cpf_modificado" in columns and "cpf_modificador" in columns:
            print("Schema da tabela Log já parece estar atualizado. Nenhuma migração necessária.")
            return

        # Verifica se a tabela tem o schema antigo (com cpf_alvo e cpf_autor)
        if "cpf_alvo" not in columns or "cpf_autor" not in columns:
             # Se não tem nem o novo nem o antigo, pode ser um estado inesperado ou a tabela não existe
             # Tentamos criar a tabela com o schema correto
             print("Tabela Log não encontrada ou com schema inesperado. Tentando criar com o schema correto...")
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
             conn.commit()
             print("Tabela Log criada com o novo schema.")
             return # Não há dados para migrar

        print("Iniciando migração do schema da tabela Log...")

        # 1. Renomear a tabela antiga
        print("Renomeando Log para Log_old...")
        cursor.execute("ALTER TABLE Log RENAME TO Log_old")
        conn.commit()

        # 2. Criar a nova tabela Log com o schema correto
        print("Criando nova tabela Log com schema atualizado...")
        cursor.execute(
            """CREATE TABLE Log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_modificador TEXT NOT NULL,
            acao TEXT NOT NULL,
            data_hora TEXT,
            cpf_modificado TEXT,
            cpf_modificador TEXT
            )"""
        )
        conn.commit()

        # 3. Migrar dados da Log_old para a nova Log
        print("Migrando dados de Log_old para Log...")
        cursor.execute("SELECT id, cpf_alvo, cpf_autor, acao, data_hora FROM Log_old")
        old_logs = cursor.fetchall()

        migrated_count = 0
        for log_id, cpf_alvo, cpf_autor, acao, data_hora in old_logs:
            nome_modificador = buscar_nome_por_cpf(conn, cpf_autor)
            try:
                cursor.execute(
                    "INSERT INTO Log (nome_modificador, acao, data_hora, cpf_modificado, cpf_modificador) VALUES (?, ?, ?, ?, ?)",
                    (nome_modificador, acao, data_hora, cpf_alvo, cpf_autor)
                )
                migrated_count += 1
            except sqlite3.Error as insert_err:
                print(f"Erro ao inserir log antigo ID {log_id} na nova tabela: {insert_err}")

        conn.commit()
        print(f"{migrated_count} registros migrados de Log_old para Log.")

        # 4. (Opcional) Remover a tabela antiga após sucesso
        # print("Removendo tabela Log_old...")
        # cursor.execute("DROP TABLE Log_old")
        # conn.commit()
        # print("Tabela Log_old removida.")
        print("Manteremos a tabela Log_old por segurança. Você pode removê-la manualmente mais tarde.")

        print("Migração do schema da tabela Log concluída com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro durante a migração do banco de dados: {e}")
        # Tentar reverter se possível (desfazer rename)
        if conn:
            try:
                print("Tentando reverter a renomeação...")
                cursor = conn.cursor()
                # Verifica se Log_old existe e Log não existe antes de renomear de volta
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Log_old'")
                log_old_exists = cursor.fetchone()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Log'")
                log_exists = cursor.fetchone()
                if log_old_exists and not log_exists:
                    cursor.execute("ALTER TABLE Log_old RENAME TO Log")
                    conn.commit()
                    print("Renomeação revertida: Log_old renomeada de volta para Log.")
                else:
                    print("Não foi possível reverter automaticamente.")
            except sqlite3.Error as revert_e:
                print(f"Erro ao tentar reverter: {revert_e}")
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    migrate_log_schema()

