const API = "http://localhost:5000/livros";

const formulario = document.getElementById("formLivro");
const lista = document.getElementById("listaLivros");
const mensagem = document.getElementById("mensagem");

async function listarLivros() {
    try {
        const resposta = await fetch(API);

        if (!resposta.ok) {
            throw new Error("Erro ao buscar os livros.");
        }

        const livros = await resposta.json();
        lista.innerHTML = "";

        if (livros.length === 0) {
            const item = document.createElement("li");
            item.textContent = "Nenhum livro cadastrado.";
            lista.appendChild(item);
            return;
        }

        livros.forEach(function(livro) {
            const item = document.createElement("li");
            const status = livro.disponivel
                ? "Disponível"
                : "Emprestado";

            item.textContent =
                livro.titulo + " - " +
                livro.autor + " (" +
                livro.ano_publicacao + ") - " +
                status;

            lista.appendChild(item);
        });
    } catch (erro) {
        mensagem.textContent =
            "Não foi possível carregar os livros. Verifique se a API está ligada.";
    }
}

formulario.addEventListener("submit", async function(evento) {
    evento.preventDefault();

    const dados = {
        titulo: document.getElementById("titulo").value.trim(),
        autor: document.getElementById("autor").value.trim(),
        ano_publicacao: document.getElementById("ano").value
    };

    try {
        const resposta = await fetch(API, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();

        if (!resposta.ok) {
            throw new Error(resultado.erro || "Erro ao cadastrar.");
        }

        mensagem.textContent = "Livro cadastrado com sucesso!";
        formulario.reset();

        await listarLivros();
    } catch (erro) {
        mensagem.textContent = erro.message ||
            "Não foi possível cadastrar o livro.";
    }
});

listarLivros();