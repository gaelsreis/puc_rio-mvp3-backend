from pydantic import BaseModel
from typing import Optional, List
from model.produto import Produto


class ProdutoSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    nome: str = "Açaí"
    quantidade: Optional[int] = 3
    valor: Optional[float] = 50.62
    tac: bool = False


class ProdutoBuscaSchemaId(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do produto.
    """
    id: int = 1


class ProdutoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do produto.
    """
    nome: str = "Açaí"


class ListagemProdutosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    produtos:List[ProdutoSchema]


def apresenta_produtos(produtos: List[Produto]):
    """ Retorna uma representação do produto seguindo o schema definido em ProdutoViewSchema.
    """
    result = []
    for produto in produtos:
        result.append({
            "id": produto.id,
            "nome": produto.nome,
            "quantidade": produto.quantidade,
            "valor": produto.valor,
            "tac": produto.tac
        })
    return {"produtos": result}


class ProdutoViewSchema(BaseModel):
    """ Define como um produto será retornado: produto
    """
    id: int = 1
    nome: str = "Açaí"
    quantidade: Optional[int] = 3
    valor: Optional[float] = 50.62
    tac: bool = False


class ProdutoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção.
    """
    mesage: str
    nome: str


class ProdutosDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção.
    """
    mesage: str


class ProdutoUpdateSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de atualização.
    """
    nome: str
    quantidade: int
    valor: float
    tac: bool


def apresenta_produto(produto: Produto):
    """ Retorna uma representação do produto seguindo o schema definido em ProdutoViewSchema.
    """
    return {
        "id": produto.id,
        "nome": produto.nome,
        "quantidade": produto.quantidade,
        "valor": produto.valor,
        "tac": produto.tac
    }