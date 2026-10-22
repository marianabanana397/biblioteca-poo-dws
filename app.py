from flask import Flask, request, jsonify
from flask_cors import CORS
from livro import Livro
from biblioteca_repository import BibliotecaRepository

app = Flask(__name__)
CORS(app)

biblioteca = BibliotecaRepository()


@app.route("/livros", methods=["GET"])
def listar_livros():
    livros = biblioteca.carregar()
    return jsonify([livro.to_dict() for livro in livros])


@app.route("/livros", methods=["POST"])
def cadastrar_livro():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie os dados do livro em JSON."}), 400

    titulo = dados.get("titulo", "")
    autor = dados.get("autor", "")
    ano = dados.get("ano_publicacao")

    if not isinstance(titulo, str) or not isinstance(autor, str):
        return jsonify({"erro": "Título e autor devem ser textos."}), 400

    titulo = titulo.strip()
    autor = autor.strip()

    if not titulo or not autor or ano is None:
        return jsonify({"erro": "Preencha todos os campos."}), 400

    try:
        ano = int(ano)
        if ano <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"erro": "Informe um ano válido."}), 400

    livros = biblioteca.carregar()
    novo_livro = Livro(titulo, autor, ano)
    livros.append(novo_livro)
    biblioteca.salvar(livros)

    return jsonify(novo_livro.to_dict()), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)