class Livro:
    def __init__(self, titulo, autor, ano_publicacao, disponivel=True):
        self.__titulo = titulo
        self.__autor = autor
        self.__ano_publicacao = ano_publicacao
        self.__disponivel = disponivel

    def to_dict(self):
        return {
            "titulo": self.__titulo,
            "autor": self.__autor,
            "ano_publicacao": self.__ano_publicacao,
            "disponivel": self.__disponivel
        }

    @classmethod
    def from_dict(cls, dados):
        return cls(
            dados["titulo"],
            dados["autor"],
            dados["ano_publicacao"],
            dados.get("disponivel", True)
        )