from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Produto
from logger import logger
from schemas import *
from flask_cors import CORS


info = Info(title="MVP-3", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
produto_tag = Tag(name="Produto", description="Visualização, adição e remoção de produtos.")


@app.get('/produtos', tags=[produto_tag], responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por produto(s)

    Retorna uma representação da listagem de produtos.
    """
    logger.debug("Coletando produtos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produtos = session.query(Produto).all()

    if not produtos:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        logger.debug("%d produtos encontrados" % len(produtos))
        # retorna a representação de produto
        print(produtos)
        return apresenta_produtos(produtos), 200


@app.post('/produto', tags=[produto_tag], responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: ProdutoSchema):
    """Adiciona um novo produto com nome, quantidade e valor.

    Retorna uma representação dos produtos.
    """
    produto = Produto(
        nome=form.nome,
        quantidade=form.quantidade,
        valor=form.valor,
        tac=form.tac)
    logger.debug(f"Adicionando produto de nome: '{produto.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(produto)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado produto: '{produto.nome}'")
        return apresenta_produto(produto), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.put('/tac', tags=[produto_tag], responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def tac_produto(query: ProdutoBuscaSchema):
    """Atualiza o status de um produto a partir do nome informado. 

    """
    produto_nome = unquote(unquote(query.nome))
    print(produto_nome)
    logger.debug(f"Atualizando dados sobre produto #{produto_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    produto = session.query(Produto).filter(Produto.nome == produto_nome).first()

    if produto:
        produto.tac = not produto.tac
        session.commit()
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Atualizando item #{produto_nome}")
        return {"mesage": "Item atualizado", "nome": produto_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Item não encontrado na base :/"
        logger.warning(
            f"Erro ao atualizar item #'{produto_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.delete('/produto', tags=[produto_tag], responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta um produto pelo nome informado

    Retorna uma mensagem de confirmação da remoção.
    """
    produto_nome = unquote(unquote(query.nome))
    print(produto_nome)
    logger.debug(f"Deletando dados sobre produto #{produto_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Produto).filter(Produto.nome == produto_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{produto_nome}")
        return {"mesage": "Produto removido", "id": produto_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado :/"
        logger.warning(f"Erro ao deletar produto #'{produto_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.delete('/limpeza', tags=[produto_tag], responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produtos():
    """Deleta todos os produtos

    Retorna uma mensagem de confirmação da remoção.
    """
    logger.debug("Limpando lista")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Produto).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug("Lista zerada")
        return {"mesage": "Produtos removidos"}
    else:
        # se o produto não foi encontrado
        error_msg = "Lista vazia :/"
        logger.warning(f"Erro ao limpar lista, {error_msg}")
        return {"mesage": error_msg}, 404
