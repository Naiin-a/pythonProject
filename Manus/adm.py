import tkinter as tk
from tkinter import messagebox, scrolledtext
from bd import BancoDeDados
from cadastro import Cadastro_adm, Cadastro
from datetime import datetime
import os
import platform
import subprocess

# Import interface functions needed by adm
# We need to be careful with circular imports if interface also imports adm
# It's generally better to structure the app differently, but we'll work with this.
try:
    # Try importing the specific functions needed
    from interface import mostrar_tela_login, abrir_cadastro
except ImportError as e:
    print(f"ERROR: Could not import required functions from interface.py: {e}")
    # Fallback or raise error might be needed depending on desired robustness
    # For now, we assume the import works or the calling functions handle it.
    mostrar_tela_login = None
    abrir_cadastro = None

# Iniciar banco de dados globalmente
bd = BancoDeDados()
bd.conectar()

# --- Funções Auxiliares --- #

def limpar_janela(janela):
    """Remove todos os widgets de uma janela."""
    for widget in janela.winfo_children():
        widget.destroy()

# --- Funções Principais do Painel ADM --- #

def mostrar_painel_adm(root, cpf_admin_logado):
    """Função principal que monta o painel de administração."""
    limpar_janela(root)
    root.title(f"Painel Administrador - ADM CPF: {cpf_admin_logado}")
    root.geometry("800x600")
    root.configure(bg="#e0e0e0")

    action_frame = tk.Frame(root, bg="#e0e0e0")
    action_frame.pack(pady=10, fill="x", padx=20)

    tk.Button(action_frame, text="Gerenciar Usuários", command=lambda: mostrar_usuarios(root, cpf_admin_logado)).pack(side="left", padx=5)
    tk.Button(action_frame, text="Gerenciar ADMs", command=lambda: mostrar_adms(root, cpf_admin_logado)).pack(side="left", padx=5)
    tk.Button(action_frame, text="Cadastrar Usuário", command=lambda: abrir_cadastro_usuario_adm(root, cpf_admin_logado)).pack(side="left", padx=5)
    tk.Button(action_frame, text="Cadastrar ADM", command=lambda: abrir_cadastro_adm(root, cpf_admin_logado)).pack(side="left", padx=5)
    tk.Button(action_frame, text="Visualizar Logs", command=lambda: visualizar_logs(root)).pack(side="left", padx=5)
    # Corrected Logout Button Call
    tk.Button(action_frame, text="Logout", command=lambda: logout_adm(root)).pack(side="right", padx=5)

    global display_frame
    display_frame = tk.Frame(root, bg="#ffffff")
    display_frame.pack(pady=10, padx=20, fill="both", expand=True)

    mostrar_usuarios(root, cpf_admin_logado)

def logout_adm(root):
    """Faz logout do ADM e volta para a tela de login."""
    if mostrar_tela_login:
        mostrar_tela_login() # Calls the function imported from interface.py
    else:
        messagebox.showerror("Erro de Logout", "Função de login não encontrada. Feche e reabra a aplicação.")

def criar_scrollable_list(parent_frame, header_texts, data_list, action_buttons_config=None):
    """Cria uma lista rolável genérica com cabeçalho e botões de ação."""
    limpar_janela(parent_frame)

    canvas = tk.Canvas(parent_frame, bg="#ffffff")
    scrollbar = tk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#ffffff")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    header_frame = tk.Frame(scrollable_frame, bg="#f0f0f0")
    header_frame.pack(fill="x", pady=(0, 5))
    col_widths = [25, 15, 25, 15] # Nome, CPF, Email/Login, Ações
    for i, text in enumerate(header_texts):
        anchor = "e" if text == "Ações" else "w"
        tk.Label(header_frame, text=text, width=col_widths[i], anchor=anchor, bg="#f0f0f0", font=("Helvetica", 10, "bold")).pack(side="left", padx=5)

    if not data_list:
        tk.Label(scrollable_frame, text="Nenhum registro encontrado.", bg="#ffffff").pack(pady=20)
    else:
        for i, item_data in enumerate(data_list):
            bg_color = "#ffffff" if i % 2 == 0 else "#f9f9f9"
            item_frame = tk.Frame(scrollable_frame, bg=bg_color)
            item_frame.pack(fill="x", pady=1)

            for j, col_text in enumerate(header_texts[:-1]):
                 data_value = item_data[j] if j < len(item_data) else "N/A"
                 tk.Label(item_frame, text=str(data_value), width=col_widths[j], anchor="w", bg=bg_color).pack(side="left", padx=5)

            if action_buttons_config:
                action_subframe = tk.Frame(item_frame, bg=bg_color)
                action_subframe.pack(side="right", padx=5)
                item_identifier = item_data[1] # Assume CPF is the second item
                for btn_text, btn_command, btn_condition in action_buttons_config:
                    if btn_condition is None or btn_condition(item_identifier):
                        tk.Button(action_subframe, text=btn_text, width=6,
                                  command=lambda id=item_identifier, cmd=btn_command: cmd(id)).pack(side="left", padx=2)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def mostrar_usuarios(root, cpf_admin_logado):
    """Exibe a lista de usuários (Pessoa) no display_frame."""
    # Limpa apenas o frame de exibição antes de adicionar o título e a lista
    limpar_janela(display_frame)
    tk.Label(display_frame, text="Gerenciamento de Usuários", font=("Helvetica", 14, "bold"), bg="#ffffff").pack(pady=5, anchor="w")
    try:
        usuarios = bd.listar_pessoas()
        data_to_display = [[u[1], u[0], u[5]] for u in usuarios] # Nome, CPF, Email
        headers = ["Nome", "CPF", "Email", "Ações"]
        actions = [
            ("Editar", lambda cpf: editar_usuario(root, cpf, cpf_admin_logado), None),
            ("Excluir", lambda cpf: excluir_usuario(root, cpf, cpf_admin_logado), None)
        ]
        criar_scrollable_list(display_frame, headers, data_to_display, actions)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar usuários: {e}", parent=root)
        limpar_janela(display_frame)
        tk.Label(display_frame, text=f"Erro ao carregar usuários: {e}", fg="red", bg="#ffffff").pack(pady=20)

def mostrar_adms(root, cpf_admin_logado):
    """Exibe a lista de Administradores no display_frame."""
    # Limpa apenas o frame de exibição antes de adicionar o título e a lista
    limpar_janela(display_frame)
    tk.Label(display_frame, text="Gerenciamento de Administradores", font=("Helvetica", 14, "bold"), bg="#ffffff").pack(pady=5, anchor="w")
    try:
        adms = bd.listar_adms()
        data_to_display = [[a[1], a[0], a[2]] for a in adms] # Nome, CPF, Login
        headers = ["Nome", "CPF", "Login", "Ações"]
        actions = [
            # ("Editar", lambda cpf: editar_adm(root, cpf, cpf_admin_logado), None), # Not implemented
            ("Excluir", lambda cpf: excluir_adm(root, cpf, cpf_admin_logado), lambda cpf_alvo: cpf_alvo != cpf_admin_logado)
        ]
        criar_scrollable_list(display_frame, headers, data_to_display, actions)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar administradores: {e}", parent=root)
        limpar_janela(display_frame)
        tk.Label(display_frame, text=f"Erro ao carregar administradores: {e}", fg="red", bg="#ffffff").pack(pady=20)

def visualizar_logs(root):
    """Abre uma nova janela para visualizar os logs formatados."""
    log_window = tk.Toplevel(root)
    log_window.title("Visualizador de Logs")
    log_window.geometry("800x600")
    log_window.transient(root)
    log_window.grab_set()

    tk.Label(log_window, text="Logs de Eventos do Sistema", font=("Helvetica", 14, "bold")).pack(pady=10)

    log_text_area = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, width=100, height=30)
    log_text_area.pack(pady=10, padx=10, fill="both", expand=True)
    log_text_area.config(state=tk.DISABLED)

    try:
        cursor = bd.conn.cursor()
        cursor.execute("SELECT id, data_hora, acao, nome_modificador, cpf_modificador, cpf_modificado FROM Log ORDER BY data_hora DESC")
        logs = cursor.fetchall()

        log_text_area.config(state=tk.NORMAL)
        log_text_area.delete("1.0", tk.END)

        if not logs:
            log_text_area.insert(tk.END, "Nenhum log encontrado.")
        else:
            log_text_area.insert(tk.END, "---- LOGS DE EVENTOS ----\n\n")
            for log in logs:
                log_id, data_hora, acao, nome_modificador, cpf_modificador, cpf_modificado = log
                log_entry = (
                    f"[{data_hora}] (ID: {log_id})\n"
                    f"  Ação: {acao}\n"
                    f"  Realizada por: {nome_modificador} (CPF: {cpf_modificador})\n"
                    f"  Alvo: CPF {cpf_modificado}\n"
                    f"------------------------------------\n"
                )
                log_text_area.insert(tk.END, log_entry)

        log_text_area.config(state=tk.DISABLED)
        tk.Button(log_window, text="Exportar para log.txt", command=exportar_logs_para_txt).pack(pady=5)
        tk.Button(log_window, text="Fechar", command=log_window.destroy).pack(pady=5)

    except Exception as e:
        # Check specifically for the 'no such column' error after migration attempt
        if "no such column" in str(e):
             messagebox.showerror("Erro de Log", f"Erro ao ler logs: {e}. O schema do banco pode não ter sido migrado corretamente. Execute o script de migração ou verifique o bd.py.", parent=log_window)
        else:
             messagebox.showerror("Erro", f"Erro ao buscar ou exibir logs: {e}", parent=log_window)
        log_text_area.config(state=tk.NORMAL)
        log_text_area.insert(tk.END, f"\nErro ao carregar logs: {e}")
        log_text_area.config(state=tk.DISABLED)

def exportar_logs_para_txt():
    """Exporta os logs formatados para um arquivo log.txt."""
    try:
        cursor = bd.conn.cursor()
        cursor.execute("SELECT id, data_hora, acao, nome_modificador, cpf_modificador, cpf_modificado FROM Log ORDER BY data_hora DESC")
        logs = cursor.fetchall()

        if not logs:
            messagebox.showinfo("Logs", "Nenhum log encontrado para exportar.")
            return

        nome_arquivo = "log.txt"
        script_dir = os.path.dirname(__file__)
        caminho_arquivo = os.path.join(script_dir, nome_arquivo)

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write("---- LOGS DE EVENTOS ----\n\n")
            for log in logs:
                log_id, data_hora, acao, nome_modificador, cpf_modificador, cpf_modificado = log
                f.write(
                    f"[{data_hora}] (ID: {log_id})\n"
                    f"  Ação: {acao}\n"
                    f"  Realizada por: {nome_modificador} (CPF: {cpf_modificador})\n"
                    f"  Alvo: CPF {cpf_modificado}\n"
                    f"------------------------------------\n"
                )

        messagebox.showinfo("Exportação Concluída", f"Logs exportados para {caminho_arquivo}")

        try:
            sistema = platform.system()
            if sistema == "Windows": os.startfile(caminho_arquivo)
            elif sistema == "Darwin": subprocess.call(["open", caminho_arquivo])
            else: subprocess.call(["xdg-open", caminho_arquivo])
        except Exception as open_e:
            messagebox.showwarning("Aviso", f"Não foi possível abrir o arquivo automaticamente: {open_e}")

    except Exception as e:
        if "no such column" in str(e):
             messagebox.showerror("Erro de Log", f"Erro ao exportar logs: {e}. O schema do banco pode não ter sido migrado corretamente.")
        else:
             messagebox.showerror("Erro", f"Erro ao exportar logs: {e}")

def editar_usuario(root, cpf_a_editar, cpf_admin_logado):
    """Abre janela para o ADM editar dados de um usuário."""
    dados_pessoa = bd.buscar_pessoa_por_cpf(cpf_a_editar)
    if not dados_pessoa:
        messagebox.showerror("Erro", "Usuário não encontrado para edição.", parent=root); return

    cpf, nome, login, _, bloco, numero_ap, email, _ = dados_pessoa

    janela_editar = tk.Toplevel(root)
    janela_editar.title(f"Editar Usuário - {nome} ({cpf})")
    janela_editar.geometry("350x450")
    janela_editar.transient(root)
    janela_editar.grab_set()

    tk.Label(janela_editar, text=f"CPF: {cpf}").pack(pady=2)
    tk.Label(janela_editar, text=f"Login: {login}").pack(pady=2)

    tk.Label(janela_editar, text="Nome").pack()
    entry_nome = tk.Entry(janela_editar); entry_nome.insert(0, nome); entry_nome.pack()
    tk.Label(janela_editar, text="Email").pack()
    entry_email = tk.Entry(janela_editar); entry_email.insert(0, email); entry_email.pack()
    tk.Label(janela_editar, text="Bloco").pack()
    entry_bloco = tk.Entry(janela_editar); entry_bloco.insert(0, str(bloco) if bloco is not None else ""); entry_bloco.pack()
    tk.Label(janela_editar, text="Número do AP").pack()
    entry_numero_ap = tk.Entry(janela_editar); entry_numero_ap.insert(0, str(numero_ap) if numero_ap is not None else ""); entry_numero_ap.pack()
    tk.Label(janela_editar, text="Nova Senha (deixe em branco para não alterar)").pack()
    entry_senha = tk.Entry(janela_editar, show="*"); entry_senha.pack()
    tk.Label(janela_editar, text="Confirmar Nova Senha").pack()
    entry_confirma_senha = tk.Entry(janela_editar, show="*"); entry_confirma_senha.pack()

    def salvar():
        novo_nome = entry_nome.get()
        novo_email = entry_email.get()
        novo_bloco_str = entry_bloco.get()
        novo_numero_ap_str = entry_numero_ap.get()
        nova_senha = entry_senha.get()
        confirma_senha = entry_confirma_senha.get()

        if not novo_nome or not novo_email:
            messagebox.showerror("Erro", "Nome e Email são obrigatórios.", parent=janela_editar); return
        try:
            novo_bloco = int(novo_bloco_str) if novo_bloco_str else None
            novo_numero_ap = int(novo_numero_ap_str) if novo_numero_ap_str else None
        except ValueError:
            messagebox.showerror("Erro", "Bloco e Número do AP devem ser números.", parent=janela_editar); return
        if nova_senha and nova_senha != confirma_senha:
            messagebox.showerror("Erro", "As senhas não coincidem.", parent=janela_editar); return

        resposta = messagebox.askyesno("Confirmar Alteração", f"Salvar mudanças para {nome} (CPF: {cpf})?", parent=janela_editar)
        if resposta:
            try:
                bd.atualizar_pessoa(cpf_modificado=cpf_a_editar, cpf_modificador=cpf_admin_logado,
                                    novo_nome=novo_nome, novo_email=novo_email, novo_bloco=novo_bloco,
                                    novo_numero_ap=novo_numero_ap, novo_senha=nova_senha if nova_senha else None)
                messagebox.showinfo("Sucesso", "Dados atualizados!", parent=janela_editar)
                janela_editar.destroy()
                mostrar_usuarios(root, cpf_admin_logado)
            except ValueError as e:
                 messagebox.showerror("Erro de Validação", str(e), parent=janela_editar)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar: {e}", parent=janela_editar)

    tk.Button(janela_editar, text="Salvar Alterações", command=salvar).pack(pady=10)
    tk.Button(janela_editar, text="Cancelar", command=janela_editar.destroy).pack(pady=5)

def excluir_usuario(root, cpf_a_excluir, cpf_admin_logado):
    """Exclui um usuário (Pessoa) pelo ADM."""
    nome_usuario = bd.buscar_nome_por_cpf(cpf_a_excluir)
    if "não encontrado" in nome_usuario or "Erro" in nome_usuario: nome_usuario = f"CPF {cpf_a_excluir}"

    resposta = messagebox.askyesno("Confirmar Exclusão", f"Excluir permanentemente o usuário {nome_usuario}?", parent=root)
    if resposta:
        try:
            if bd.deletar_pessoa(cpf_modificado=cpf_a_excluir, cpf_modificador=cpf_admin_logado):
                messagebox.showinfo("Sucesso", f"Usuário {nome_usuario} excluído!", parent=root)
                mostrar_usuarios(root, cpf_admin_logado)
            else:
                 messagebox.showwarning("Aviso", f"Usuário {nome_usuario} não encontrado.", parent=root)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir usuário: {e}", parent=root)

def excluir_adm(root, cpf_a_excluir, cpf_admin_logado):
    """Exclui um Administrador pelo ADM."""
    if cpf_a_excluir == cpf_admin_logado:
        messagebox.showerror("Erro", "Você não pode excluir sua própria conta de administrador.", parent=root)
        return

    nome_adm = bd.buscar_nome_por_cpf(cpf_a_excluir)
    if "não encontrado" in nome_adm or "Erro" in nome_adm: nome_adm = f"ADM CPF {cpf_a_excluir}"

    resposta = messagebox.askyesno("Confirmar Exclusão de ADM", f"Excluir permanentemente o administrador {nome_adm}?", parent=root)
    if resposta:
        try:
            if bd.deletar_adm(cpf_modificado=cpf_a_excluir, cpf_modificador=cpf_admin_logado):
                messagebox.showinfo("Sucesso", f"Administrador {nome_adm} excluído!", parent=root)
                mostrar_adms(root, cpf_admin_logado)
            else:
                 messagebox.showwarning("Aviso", f"Administrador {nome_adm} não encontrado.", parent=root)
        except ValueError as e:
             messagebox.showerror("Erro", str(e), parent=root)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir administrador: {e}", parent=root)

def abrir_cadastro_usuario_adm(root, cpf_admin_logado):
    """Abre janela para ADM cadastrar novo usuário (Pessoa)."""
    if abrir_cadastro: # Check if function was imported successfully
        abrir_cadastro(cpf_admin_logado) # Calls the function imported from interface.py
    else:
        messagebox.showerror("Erro", "Função de cadastro não encontrada.")

def abrir_cadastro_adm(root, cpf_admin_logado):
    """Abre janela para ADM cadastrar novo ADM."""
    cadastro_window = tk.Toplevel(root)
    cadastro_window.title("Cadastro de Novo Administrador")
    cadastro_window.geometry("350x350")
    cadastro_window.transient(root)
    cadastro_window.grab_set()

    labels = ["CPF (11 dígitos)", "Login", "Nome Completo", "Senha", "Confirmar Senha"]
    entries = {}
    for label_text in labels:
        tk.Label(cadastro_window, text=label_text).pack()
        entry = tk.Entry(cadastro_window, show="*" if "Senha" in label_text else "")
        entry.pack()
        entries[label_text.split(" (")[0].replace(" ", "_").lower()] = entry

    def cadastrar():
        cpf = entries["cpf"].get()
        login = entries["login"].get()
        nome = entries["nome_completo"].get()
        senha = entries["senha"].get()
        confirma_senha = entries["confirmar_senha"].get()

        if not all([cpf, login, nome, senha, confirma_senha]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.", parent=cadastro_window); return
        if not cpf.isdigit() or len(cpf) != 11:
             messagebox.showerror("Erro", "CPF inválido.", parent=cadastro_window); return
        if senha != confirma_senha:
            messagebox.showerror("Erro", "As senhas não coincidem.", parent=cadastro_window); return

        try:
            adm = Cadastro_adm(cpf=cpf, login=login, nome=nome, senha=senha,
                               data_cadastro=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            bd.inserir_adm(adm, cpf_admin_logado)
            messagebox.showinfo("Sucesso", "Administrador cadastrado!", parent=cadastro_window)
            cadastro_window.destroy()
            mostrar_adms(root, cpf_admin_logado)
        except ValueError as e:
            messagebox.showerror("Erro de Cadastro", str(e), parent=cadastro_window)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}", parent=cadastro_window)

    tk.Button(cadastro_window, text="Cadastrar ADM", command=cadastrar).pack(pady=10)
    tk.Button(cadastro_window, text="Cancelar", command=cadastro_window.destroy).pack(pady=5)

# --- Ponto de Entrada (se executado diretamente) --- #
if __name__ == '__main__':
    # This part is for testing the adm panel directly.
    # It might fail if interface.py cannot be imported or has issues.
    print("Attempting to run adm.py directly for testing...")
    test_root = tk.Tk()
    cpf_admin_teste = "00000000000" # Use a valid Admin CPF from your DB
    try:
        # Ensure test admin exists
        cursor = bd.conn.cursor()
        cursor.execute("SELECT 1 FROM Adm WHERE cpf = ?", (cpf_admin_teste,))
        if not cursor.fetchone():
             print(f"Test Admin {cpf_admin_teste} not found. Creating...")
             test_adm = Cadastro_adm(cpf_admin_teste, 'adm_test', 'Admin Teste', 'test123', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
             bd.inserir_adm(test_adm, cpf_admin_teste) # Self-registration

        mostrar_painel_adm(test_root, cpf_admin_teste)
        test_root.mainloop()
    except Exception as main_e:
        print(f"Error starting Admin panel for testing: {main_e}")
    finally:
        bd.fechar_conexao()

