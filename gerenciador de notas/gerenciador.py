from pathlib import Path
import json
from typing import List, Dict

class Aluno:
    """
    Representa um aluno com nome e nota

    Atributos:
        nome (str): Nome do aluno
        nota (float): Nota do aluno
    """
    def __init__(self, nome: str, nota: float):
        """
        Inicializa uma nova instância de Aluno.

        Args:
        nome (str): Nome do aluno
        nota (float): Nota do aluno
        """
        self.nome = nome.strip().title()
        self.nota = float(nota)

    def to_dict(self) -> Dict[str, float]:
        """
        Retorna o aluno como um dicionario com nome e nota.

        returns:
            dict Um dicionario {nome: nota}
        """
        return {self.nome: self.nota}

    def __str__(self) -> str:
        """
        Representação em string do aluno formato CSV

        returns:
        str: Nome e nota separados por virgula.

        """
        return f"{self.nome}, {self.nota:.1f}"

class GerenciadorAlunos:
    """
    Classe responsavel pelo gerenciamento de alunos e persistencia dos dados.

    Attributes:
        csv_path (Path): Caminho do arquivo CSV.
        json_path (Path): Caminho do arquivo JSON.
        txt_path (Path): Caminho do arquivo TXT.
        alunos (Dict[str, float]): Dicionario com os dados dos alunos.
    """
    def __init__(self, base_dir: Path):
        """
        Inicializa o gerenciador e carrega os dados existentes.

        Args:
        base_dir (Path): Diretorio base onde os arquivos serão armazenados.
        """

        self.csv_path = base_dir / "alunos.csv"
        self.json_path = base_dir / "alunos.json"
        self.txt_path = base_dir / "alunos.txt"
        self.alunos: Dict[str, float] = self._carregar()

    def _carregar(self) -> Dict[str, float]:
        """
        Carrega os dados dos alunos a partir do arquivo CSV, se existir. (_ == Método protegido ou interno)
        Returns:
            dict: Dicionario comos dados dos alunos.
        """

        if self.csv_path.exists():
            try:
                with open(self.csv_path, "r") as f:
                    return {
                        nome: float(nota)
                        for nome, nota in (linha.strip().split(",") for linha in f)
                    }

            except FileNotFoundError:
                print("Arquivo CSV não encontrado.")
            except ValueError as ve:
                print(f"Erro ao converter nota para float: {ve}")
            except OSError as oe:
                print(f"Erro de sistema ao acessar o arquivo: {oe}")

        return {}

    def salvar(self) -> None:
        """
        Salva os dados dos alunos nos formatos CSV, TXT e JSON.

        """
        try:
            with open(self.csv_path, "w") as f_csv, open(self.txt_path, "w") as f_txt, open(self.json_path, "w") as f_json:
                for nome, nota in self.alunos.items():
                    linha = f"{nome},{nota:1f}\n"
                    f_csv.write(linha)
                    f_txt.write(f"{nome} tem nota {nota:1f}\n")
                json.dump(self.alunos, f_json, indent=4)
        except Exception as e:
            print(f"Erro ao salvar os arquivos: {e}")

    def cadastrar(self, aluno: Aluno) -> bool:
        """
        Cadastra ou atualiza um aluno no dicionario e salva os dados.

        Args:
            aluno (Aluno): Instancia da clase aluno

        Returns:
            bool: True se o cadastro foi bem-sucedido.

        """

        self.alunos[aluno.nome] = aluno.nota
        self.salvar()
        return True

    def remover(self, nome: str) -> bool:
        """
            Remove um aluno nome.
        Args:
            nome (str): Nome do aluno a ser removido.
        Returns:
            bool: True se o aluno foi removido, False caso contrario.
        """

        if nome in self.alunos:
            del self.alunos[nome]
            self.salvar()
            return True

        return False

    def alterar_nota(self, nome: str, nova_nota: float) -> bool:
        """
        Altera a nota de um aluno existente.

        args:
            nome (str): Nome do aluno.
            nova_nota (float): Nova nota a ser atribuida.

        returns:
            bool: True se a nota foi alterada, False caso o aluno não exista

        """
        if nome in self.alunos:
            self.alunos[nome] = nova_nota
            self.salvar()
            return True
        return False

    def listar(self) -> List[str]:
        """
        Lista todos os alunos cadastrados

        return:
        list: Lista de strings no formato "nome, nota".
        """
        return [f"{nome}, {nota:.1f}" for nome , nota in self.alunos.items()]

    def buscar(self, nome: str) -> str:
        """
            Busca um aluno pelo nome.
        Args:
            nome(str): Nome do aluno.

        Returns:
            str: Informação do aluno no formato "nome, nota" ou mensagem de erro.
        """

        if nome in self.alunos:
            return f"{nome}, {self.alunos[nome]:.1f}"
        return "Aluno não encontrado."


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    gerenciador = GerenciadorAlunos(base_dir)

    print("Cadastrado:", gerenciador.cadastrar(Aluno("Paulo", 7)))
    print("Lendo:", gerenciador.buscar("Paulo"))
    print("Lista completa:", gerenciador.listar())
    print("Removendo: ", gerenciador.remover("Paulo"))
    print("Lista pos remoção: ", gerenciador.listar())
    print("Novo cadastro: ", gerenciador.cadastrar(Aluno("Maria", 7)))
    print("Alterando nota:", gerenciador.alterar_nota("Maria", 10))
    print("Lista final:", gerenciador.listar())
