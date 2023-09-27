from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Produto(Base):
    __tablename__ = 'produto'

    id = Column("pk_produto", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    quantidade = Column(Integer)
    valor = Column(Float)
    tac = Column(Boolean)
    data_insercao = Column(DateTime, default=datetime.now())


    def __init__(self, nome:str, quantidade:int, valor:float, tac:bool,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Produto

        Arguments:
            nome: nome do produto.
            quantidade: quantidade que se espera comprar daquele produto
            valor: valor esperado para o produto
            data_insercao: data de quando o produto foi inserido à base
        """
        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor
        self.tac = tac

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao