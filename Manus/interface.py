import tkinter as tk
from tkinter import messagebox
from bd import BancoDeDados
from cadastro import Cadastro
from datetime import datetime

# Iniciar banco de dados
bd = BancoDeDados()
bd.conectar()
# REMOVIDO: bd.criar_tabelas() # A criação/verificação agora é feita em bd.conectar()

# Variável global para armazenar o CPF do usuário logado
cpf_usuario_logado_global = None
nome_usuario_logado_global = None

# Janela principal
root = tk.Tk()
root.title("Sistema de Login")
root.configure(bg="gray")
root.geometry("300x300")

def limpar_janela(janela):
    """Remove todos os widgets de uma janela."""
    for widget in janela.winfo_children():
        widget.destroy()

def mostrar_tela_login():
    """Configura e exibe a tela de login inicial."""
    global cpf_usuario_logado_global, nome_usuario_logado_global
    cpf_usuario_logado_global = None # Limpa o usuário logado ao voltar para o login
    nome_usuario_logado_global = None

    limpar_janela(root)
    root.title("Sistema de Login")
    root.geometry("300x300")
    root.configure(bg="gray")

    tk.Label(root, text="Login", bg="gray").pack()
    entry_login = tk.Entry(root)
    entry_login.pack()

    tk.Label(root, text="Senha", bg="gray").pack()
    entry_senha = tk.Entry(root, show="*")
    entry_senha.pack()

    tk.Button(root, text="Entrar", command=lambda: fazer_login(entry_login.get(), entry_senha.get())).pack(pady=10)
    tk.Button(root, text="Cadastrar", command=lambda: abrir_cadastro(None)).pack() # None indica auto-cadastro


def mostrar_dados_usuario(cpf_usuario_logado, nome_usuario_logado):
    """Exibe os dados do usuário logado."""
    global cpf_usuario_logado_global, nome_usuario_logado_global
    cpf_usuario_logado_global = cpf_usuario_logado # Atualiza o CPF global
    nome_usuario_logado_global = nome_usuario_logado

    dados_pessoa = bd.buscar_pessoa_por_cpf(cpf_usuario_logado)

    if not dados_pessoa:
        messagebox.showerror("Erro", f"Não foi possível encontrar os dados para o CPF: {cpf_usuario_logado}")
        mostrar_tela_login() # Volta para o login se não encontrar dados
        return

    # Extrai dados (ignorando senha e data_cadastro que não são exibidos aqui)
    cpf, nome, login, _, bloco, numero_ap, email, _ = dados_pessoa

    limpar_janela(root)
    janela_dados = root
    janela_dados.title(f"Dados do Usuário - {nome}")
    janela_dados.geometry("400x300")
    janela_dados.configure(bg="#f0f8ff")

    tk.Label(janela_dados, text="Informações do Usuário", font=("Helvetica", 14, "bold"), bg="#f0f8ff").pack(pady=10)

    info_map = {
        "Nome": nome,
        "CPF": cpf,
        "Login": login,
        "Bloco": bloco if bloco is not None else "N/A",
        "Apartamento": numero_ap if numero_ap is not None else "N/A",
        "Email": email
    }

    for label, value in info_map.items():
        tk.Label(janela_dados, text=f"{label}: {value}", anchor="w", justify="left", bg="#f0f8ff").pack(fill="x", padx=15, pady=4)

    # Botões para Editar ou Excluir
    tk.Button(janela_dados, text="Editar Meus Dados", command=lambda: editar_dados_usuario(cpf_usuario_logado)).pack(pady=5)
    tk.Button(janela_dados, text="Excluir Minha Conta", command=lambda: excluir_conta(cpf_usuario_logado)).pack(pady=5)
    tk.Button(janela_dados, text="Logout", command=mostrar_tela_login).pack(pady=10)


def editar_dados_usuario(cpf_a_editar):
    """Abre a janela para editar os dados do usuário logado."""
    global cpf_usuario_logado_global # Precisa do CPF de quem está fazendo a edição

    dados_pessoa = bd.buscar_pessoa_por_cpf(cpf_a_editar)

    if not dados_pessoa:
        messagebox.showerror("Erro", "Usuário não encontrado para edição.")
        return

    # Desempacota todos os dados retornados pela busca
    cpf, nome, login, senha_atual, bloco, numero_ap, email, data_cadastro = dados_pessoa

    # Criação de nova janela para editar os dados
    editar_window = tk.Toplevel(root)
    editar_window.title("Editar Meus Dados")
    editar_window.geometry("350x450")
    editar_window.transient(root)
    editar_window.grab_set()

    # Campos não editáveis (CPF e Login geralmente não mudam)
    tk.Label(editar_window, text=f"CPF: {cpf}").pack(pady=2)
    tk.Label(editar_window, text=f"Login: {login}").pack(pady=2)

    # Campos editáveis
    tk.Label(editar_window, text="Nome").pack()
    entry_nome_edit = tk.Entry(editar_window)
    entry_nome_edit.insert(0, nome)
    entry_nome_edit.pack()

    tk.Label(editar_window, text="Email").pack()
    entry_email_edit = tk.Entry(editar_window)
    entry_email_edit.insert(0, email)
    entry_email_edit.pack()

    tk.Label(editar_window, text="Bloco").pack()
    entry_bloco_edit = tk.Entry(editar_window)
    entry_bloco_edit.insert(0, str(bloco) if bloco is not None else "")
    entry_bloco_edit.pack()

    tk.Label(editar_window, text="Número do AP").pack()
    entry_numero_ap_edit = tk.Entry(editar_window)
    entry_numero_ap_edit.insert(0, str(numero_ap) if numero_ap is not None else "")
    entry_numero_ap_edit.pack()

    # Campos de senha
    tk.Label(editar_window, text="Nova Senha (deixe em branco para não alterar)").pack()
    entry_senha_edit = tk.Entry(editar_window, show="*")
    entry_senha_edit.pack()

    tk.Label(editar_window, text="Confirmar Nova Senha").pack()
    entry_confirma_senha_edit = tk.Entry(editar_window, show="*")
    entry_confirma_senha_edit.pack()

    def salvar_edicao():
        novo_nome = entry_nome_edit.get()
        novo_email = entry_email_edit.get()
        novo_bloco_str = entry_bloco_edit.get()
        novo_numero_ap_str = entry_numero_ap_edit.get()
        nova_senha = entry_senha_edit.get()
        confirma_senha = entry_confirma_senha_edit.get()

        # Validação básica de entrada
        if not novo_nome or not novo_email:
            messagebox.showerror("Erro", "Nome e Email são obrigatórios.", parent=editar_window)
            return

        try:
            novo_bloco = int(novo_bloco_str) if novo_bloco_str else None
            novo_numero_ap = int(novo_numero_ap_str) if novo_numero_ap_str else None
        except ValueError:
            messagebox.showerror("Erro", "Bloco e Número do AP devem ser números.", parent=editar_window)
            return

        if nova_senha and nova_senha != confirma_senha:
            messagebox.showerror("Erro", "As senhas não coincidem.", parent=editar_window)
            return

        try:
            # Chama a função atualizada do BD, passando o CPF de quem está logado como modificador
            bd.atualizar_pessoa(
                cpf_modificado=cpf_a_editar,
                cpf_modificador=cpf_usuario_logado_global, # CPF de quem está logado
                novo_nome=novo_nome,
                novo_email=novo_email,
                novo_bloco=novo_bloco,
                novo_numero_ap=novo_numero_ap,
                novo_senha=nova_senha if nova_senha else None # Passa None se a senha não for alterada
            )
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!", parent=editar_window)
            editar_window.destroy()
            # Atualiza a tela principal com os novos dados
            mostrar_dados_usuario(cpf_usuario_logado_global, novo_nome) # Usa o nome atualizado
        except ValueError as e:
             messagebox.showerror("Erro de Validação", str(e), parent=editar_window)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar dados: {e}", parent=editar_window)

    tk.Button(editar_window, text="Salvar Alterações", command=salvar_edicao).pack(pady=10)
    tk.Button(editar_window, text="Cancelar", command=editar_window.destroy).pack(pady=5)

def excluir_conta(cpf_a_excluir):
    """Exclui a conta do usuário logado."""
    global cpf_usuario_logado_global

    resposta = messagebox.askyesno("Excluir Conta", "Você tem certeza que deseja excluir sua conta permanentemente? Esta ação não pode ser desfeita.")
    if resposta:
        try:
            # Chama a função atualizada do BD, passando o CPF de quem está logado como modificador
            if bd.deletar_pessoa(cpf_modificado=cpf_a_excluir, cpf_modificador=cpf_usuario_logado_global):
                messagebox.showinfo("Sucesso", "Conta excluída com sucesso!")
                mostrar_tela_login() # Volta para a tela de login após exclusão
            else:
                 messagebox.showwarning("Aviso", "Não foi possível encontrar a conta para exclusão.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir conta: {e}")

def fazer_login(login, senha):
    """Tenta fazer login como ADM ou Pessoa."""
    global cpf_usuario_logado_global, nome_usuario_logado_global

    if not login or not senha:
        messagebox.showerror("Erro", "Login e Senha são obrigatórios.")
        return

    resultado_login = bd.validar_login(login, senha)

    if resultado_login:
        tipo_usuario, cpf_logado, nome_logado = resultado_login
        cpf_usuario_logado_global = cpf_logado # Armazena o CPF globalmente
        nome_usuario_logado_global = nome_logado

        if tipo_usuario == "Adm":
            messagebox.showinfo("Sucesso", f"Login de administrador bem-sucedido! Bem-vindo, {nome_logado}.")
            # Importa a função do adm aqui para evitar dependência circular no topo
            try:
                from adm import mostrar_painel_adm
                mostrar_painel_adm(root, cpf_usuario_logado_global) # Passa o CPF do admin logado
            except ImportError:
                 messagebox.showerror("Erro", "Não foi possível carregar o painel administrativo.")
                 mostrar_tela_login()
        elif tipo_usuario == "Pessoa":
            messagebox.showinfo("Sucesso", f"Login de usuário bem-sucedido! Bem-vindo, {nome_logado}.")
            mostrar_dados_usuario(cpf_logado, nome_logado)
        else:
             messagebox.showerror("Erro", "Tipo de usuário desconhecido.")
             mostrar_tela_login()
    else:
        messagebox.showerror("Erro", "Login ou senha inválidos.")

def abrir_cadastro(cpf_modificador):
    """Abre a janela para cadastro de um novo usuário (Pessoa)."""
    # Se cpf_modificador for None, significa que é um auto-cadastro (tela de login)
    # Se tiver um valor, é um admin cadastrando (vindo do painel adm)
    quem_cadastra = cpf_modificador if cpf_modificador else "auto-cadastro"

    cadastro_window = tk.Toplevel(root)
    cadastro_window.title("Cadastro de Novo Usuário")
    cadastro_window.geometry("350x450")
    cadastro_window.transient(root)
    cadastro_window.grab_set()

    # Campos de cadastro
    labels = ["CPF (11 dígitos)", "Login", "Nome Completo", "Senha", "Confirmar Senha", "Bloco", "Número do AP", "Email"]
    entries = {}

    for i, label_text in enumerate(labels):
        tk.Label(cadastro_window, text=label_text).pack()
        entry = tk.Entry(cadastro_window, show="*" if "Senha" in label_text else "")
        entry.pack()
        # Usa uma chave sem espaços para o dicionário
        entries[label_text.split(" (")[0].replace(" ", "_").lower()] = entry

    def cadastrar_pessoa():
        # Coleta os dados dos entries
        cpf = entries["cpf"].get()
        login = entries["login"].get()
        nome = entries["nome_completo"].get()
        senha = entries["senha"].get()
        confirma_senha = entries["confirmar_senha"].get()
        bloco_str = entries["bloco"].get()
        numero_ap_str = entries["número_do_ap"].get()
        email = entries["email"].get()

        # Validações
        if not all([cpf, login, nome, senha, confirma_senha, email]):
            messagebox.showerror("Erro", "Todos os campos, exceto Bloco e AP, são obrigatórios.", parent=cadastro_window)
            return
        if not cpf.isdigit() or len(cpf) != 11:
             messagebox.showerror("Erro", "CPF inválido. Deve conter 11 dígitos numéricos.", parent=cadastro_window)
             return
        if senha != confirma_senha:
            messagebox.showerror("Erro", "As senhas não coincidem.", parent=cadastro_window)
            return

        try:
            bloco = int(bloco_str) if bloco_str else None
            numero_ap = int(numero_ap_str) if numero_ap_str else None
        except ValueError:
            messagebox.showerror("Erro", "Bloco e Número do AP devem ser números.", parent=cadastro_window)
            return

        try:
            pessoa = Cadastro(
                cpf=cpf,
                login=login,
                nome=nome,
                senha=senha,
                bloco=bloco,
                numero_ap=numero_ap,
                email=email,
                data_cadastro=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            # Determina o CPF do modificador
            cpf_do_modificador = cpf_modificador if cpf_modificador else cpf

            bd.inserir_pessoa(pessoa, cpf_do_modificador)
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!", parent=cadastro_window)
            cadastro_window.destroy()

        except ValueError as e: # Captura erros de CPF/Login/Email duplicado do BD
            messagebox.showerror("Erro de Cadastro", str(e), parent=cadastro_window)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado ao cadastrar: {e}", parent=cadastro_window)

    tk.Button(cadastro_window, text="Cadastrar", command=cadastrar_pessoa).pack(pady=10)
    tk.Button(cadastro_window, text="Cancelar", command=cadastro_window.destroy).pack(pady=5)

# Função para ser chamada pelo adm.py para abrir o cadastro
def abrir_cadastro_via_adm(parent_root, cpf_admin_logado):
    abrir_cadastro(cpf_admin_logado)

# Função principal para iniciar a interface (pode ser chamada pelo adm.py no logout)
def iniciar_interface(master_root):
    global root
    root = master_root # Reutiliza a janela principal
    mostrar_tela_login()

# --- Ponto de Entrada Principal --- #
if __name__ == "__main__":
    iniciar_interface(root) # Inicia a aplicação mostrando a tela de login

    # Garante que a conexão com o banco seja fechada ao sair
    root.protocol("WM_DELETE_WINDOW", lambda: (bd.fechar_conexao(), root.destroy()))

    root.mainloop()

