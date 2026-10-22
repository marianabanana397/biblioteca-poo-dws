import sqlite3
from livro import Livro


class BibliotecaRepository:
    def __init__(self, caminho_arquivo="biblioteca.db"):
        self.caminho_arquivo = caminho_arquivo
        self.criar_tabela()

    def conectar(self):
        return sqlite3.connect(self.caminho_arquivo)

    def criar_tabela(self):
        with self.conectar() as conexao:
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS livros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    ano_publicacao INTEGER NOT NULL,
                    disponivel INTEGER NOT NULL DEFAULT 1
                )
            """)

    def salvar(self, livros):
        with self.conectar() as conexao:
            conexao.execute("DELETE FROM livros")

            for livro in livros:
                dados = livro.to_dict()

                conexao.execute("""
                    INSERT INTO livros
                    (titulo, autor, ano_publicacao, disponivel)
                    VALUES (?, ?, ?, ?)
                """, (
                    dados["titulo"],
                    dados["autor"],
                    dados["ano_publicacao"],
                    int(dados["disponivel"])
                ))

    def carregar(self):
        with self.conectar() as conexao:
            registros = conexao.execute("""
                SELECT titulo, autor, ano_publicacao, disponivel
                FROM livros
                ORDER BY id
            """).fetchall()

        return [
            Livro(titulo, autor, ano, bool(disponivel))
            for titulo, autor, ano, disponivel in registros
        ]