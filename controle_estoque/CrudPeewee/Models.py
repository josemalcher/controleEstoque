# -*- coding: utf-8 -*-
import sys
import os
import configparser

from Crud.Conexao import Conexao
from Crud.Conexao import CreateDb
from Crud.Conexao import BaseModel
from peewee import DatabaseError
from peewee import InternalError
from peewee import IntegerField
from peewee import ForeignKeyField
from peewee import DecimalField
from peewee import BigBitField
from peewee import CharField
from peewee import PrimaryKeyField
from peewee import DateField
from peewee import Field
from playhouse.mysql_ext import MySQLConnectorDatabase
from playhouse.pool import PooledMySQLDatabase


# Classe campo personalizado longblob
class LongBlobCampo(Field):
    field_type = 'LONGBLOB'


# Tabela Categoria de produtos
class CategoriaProduto(BaseModel):
    id = PrimaryKeyField(null=False)
    categoria_produto = CharField(max_length=100)

    class Meta:
        db_table = 'categoria_produto'


# Tabela Marca Produtos
class MarcaProduto(BaseModel):
    id = PrimaryKeyField(null=False)
    marca_produto = CharField(max_length=50)

    class Meta:
        db_table = 'marca_produto'


# Tabela Produtos
class Produto(BaseModel):
    id = PrimaryKeyField(null=False)
    produto = CharField(max_length=80)
    imagem = LongBlobCampo()
    categoria = ForeignKeyField(CategoriaProduto, column_name='categoria')
    marca = ForeignKeyField(MarcaProduto, column_name='marca')
    estoque_minimo = IntegerField(default=0)
    estoque_maximo = IntegerField(default=0)
    qtde = IntegerField(default=0)
    valor_compra = DecimalField(9, 2)
    valor_unitario = DecimalField(9, 2)
    valor_atacado = DecimalField(9, 2)
    qtde_atacado = IntegerField(default=5)
    obs = CharField(max_length=80)

    class Meta:
        db_table = 'produto'


# Tabela Clientes
class Cliente(BaseModel):
    id = PrimaryKeyField(null=False)
    nome = CharField(max_length=50)
    sobrenome = CharField(max_length=50)
    cpf = CharField(max_length=15)
    rg = CharField(max_length=15)
    celular = CharField(max_length=15)
    telefone = CharField(max_length=15)
    email = CharField(max_length=50)
    obs = CharField(max_length=50)
    cep = CharField(max_length=12)
    endereco = CharField(max_length=50)
    numero = CharField(max_length=5)
    bairro = CharField(max_length=40)
    cidade = CharField(max_length=40)
    estado = CharField(max_length=2)

    class Meta:
        db_table = 'cliente'


#  Tabela Fornecedor
class Fornecedor(BaseModel):
    id = PrimaryKeyField(null=False)
    nome_fantasia = CharField(max_length=80)
    razao_social = CharField(max_length=(80))
    cnpj = CharField(max_length=20)
    insc_estadual = CharField(max_length=20)
    telefone = CharField(max_length=20)
    email = CharField(max_length=80)
    site = CharField(max_length=80)
    obs = CharField(max_length=100)
    cep = CharField(max_length=12)
    endereco = CharField(max_length=50)
    numero = CharField(max_length=5)
    bairro = CharField(max_length=40)
    cidade = CharField(max_length=40)
    estado = CharField(max_length=2)

    class Meta:
        db_table = 'fornecedor'


# Tabela Categoria a pagar
class CatAPagar(BaseModel):
    id = PrimaryKeyField(null=False)
    categoria_a_pagar = CharField(max_length=80)

    class Meta:
        db_table = 'categoria_a_pagar'


# Tabela Categoria a Receber
class CatAReceber(BaseModel):
    id = PrimaryKeyField(null=False)
    categoria_a_receber = CharField(max_length=80)

    class Meta:
        db_table = 'categoria_a_receber'


# Tabela Forma de Pagamento
class FormaPagamento(BaseModel):
    id = PrimaryKeyField(null=False)
    forma_pagamento = CharField(max_length=80)

    class Meta:
        db_table = 'forma_de_pagamento'


# Tabela Status Pagamento
class StatusPagamento(BaseModel):
    id = PrimaryKeyField(null=False)
    status_pagamento = CharField(max_length=80)

    class Meta:
        db_table = 'status_pagamento'


# Tabela Status Entrega
class StatusEntrega(BaseModel):
    id = PrimaryKeyField(null=False)
    status_entrega = CharField(max_length=80)

    class Meta:
        db_table = 'status_entrega'


# Tabela Compras
class Compra(BaseModel):
    id = PrimaryKeyField(null=False)
    id_fornecedor = ForeignKeyField(Fornecedor, column_name='id_fornecedor')
    data_emissao = DateField()
    prazo_entrega = DateField()
    data_entrega = DateField()
    categoria = ForeignKeyField(CatAPagar, column_name='categoria')
    desconto = DecimalField(9, 2)
    frete = DecimalField(9, 2)
    valor_total = DecimalField(9, 2)
    valor_pago = DecimalField(9, 2)
    valor_pendente = DecimalField(9, 2)
    entrega = ForeignKeyField(
        StatusEntrega, column_name='entrega', default='2')
    pagamento = ForeignKeyField(
        StatusPagamento, column_name='pagamento', default='2')

    class Meta:
        db_table = 'compra'


# Tabela relação de item comprados (carrinho de compra)
class RelacaoCompra(BaseModel):
    id = CharField(max_length=25, primary_key=True)
    id_compra = ForeignKeyField(Compra, column_name='id_compra')
    id_produto = ForeignKeyField(Produto, column_name='id_produto')
    qtde = DecimalField(9, 2)
    valor_unitario = DecimalField(9, 2)
    valor_total = DecimalField(9, 2)
    obs = CharField(max_length=80)

    class Meta:
        db_table = 'relacao_compra'


# Tabela Vendas
class Venda(BaseModel):
    id = PrimaryKeyField(null=False)
    id_cliente = ForeignKeyField(
        Cliente, column_name='id_cliente')
    data_emissao = DateField()
    prazo_entrega = DateField()
    data_entrega = DateField()
    categoria = ForeignKeyField(
        CatAReceber, column_name='categoria')
    desconto = DecimalField(9, 2)
    frete = DecimalField(9, 2)
    valor_total = DecimalField(9, 2)
    valor_recebido = DecimalField(9, 2)
    valor_pendente = DecimalField(9, 2)
    entrega = ForeignKeyField(
        StatusEntrega, column_name='entrega', default='2')
    pagamento = ForeignKeyField(
        StatusPagamento, column_name='pagamento', default='2')

    class Meta:
        db_table = 'venda'


# Tabela relação de item comprados (carrinho de compra)
class RelacaoVenda(BaseModel):
    id = CharField(max_length=25, primary_key=True)
    id_venda = ForeignKeyField(Venda, column_name='id_venda')
    id_produto = ForeignKeyField(Produto, column_name='id_produto')
    qtde = DecimalField(9, 2)
    valor_unitario = DecimalField(9, 2)
    valor_total = DecimalField(9, 2)
    obs = CharField(max_length=80)

    class Meta:
        db_table = 'relacao_venda'


# Tabela Contas a Pagar
class ContaAPagar(BaseModel):
    id = PrimaryKeyField(null=False)
    id_compra = ForeignKeyField(Compra, column_name='id_compra', null=True)
    id_fornecedor = ForeignKeyField(Fornecedor, column_name='id_fornecedor')
    descricao = CharField(max_length=150)
    obs = CharField(max_length=150)
    categoria = ForeignKeyField(CatAPagar, column_name='categoria')
    data_vencimento = DateField()
    valor = DecimalField(9, 2)
    forma_pagamento = ForeignKeyField(
        FormaPagamento, column_name='forma_pagamento')
    data_pagamento = DateField()
    valor_pago = DecimalField(9, 2)
    status_pagamento = ForeignKeyField(StatusPagamento, column_name='status_pagamento',
                                       default=2)

    class Meta:
        db_table = 'conta_a_pagar'


# Tabela Contas a Receber
class ContaAReceber(BaseModel):
    id = PrimaryKeyField(null=False)
    id_venda = ForeignKeyField(Venda, column_name='id_venda', null=True)
    id_cliente = ForeignKeyField(Cliente, column_name='id_cliente')
    descricao = CharField(max_length=150)
    obs = CharField(max_length=150)
    categoria = ForeignKeyField(CatAReceber, column_name='categoria')
    data_vencimento = DateField()
    valor = DecimalField(9, 2)
    forma_pagamento = ForeignKeyField(
        FormaPagamento, column_name='forma_pagamento')
    data_recebimento = DateField()
    valor_recebido = DecimalField(9, 2)
    status_pagamento = ForeignKeyField(
        StatusPagamento, column_name='status_pagamento', default=2)

    class Meta:
        db_table = 'conta_a_receber'


# Tabela Com os dados da Empresa

class Empresa(BaseModel):
    id = PrimaryKeyField(null=False)
    nome_fantasia = CharField(max_length=80)
    razao_social = CharField(max_length=(80))
    cnpj = CharField(max_length=20)
    insc_estadual = CharField(max_length=20)
    telefone = CharField(max_length=20)
    email = CharField(max_length=80)
    site = CharField(max_length=80)
    obs = CharField(max_length=80)
    cep = CharField(max_length=12)
    endereco = CharField(max_length=50)
    numero = CharField(max_length=5)
    bairro = CharField(max_length=40)
    cidade = CharField(max_length=40)
    estado = CharField(max_length=2)
    titulo = CharField(max_length=20)
    subtitulo = CharField(max_length=80)
    logo = LongBlobCampo()

    class Meta:
        db_table = 'empresa'


# Criando todas as tabelas e inserindo valores padrão
class CriarTabelas(object):
    def __init__(self, teste=""):
        self.teste = teste
        pass

    def tabelas(self):
        try:
            models = [Cliente, Fornecedor, CatAPagar]

            # Conexao().dbhandler.close()
            # Criando Tabelas
            # Conexao().dbhandler.create_tables([
            #     CategoriaProduto,
            #     MarcaProduto,
            #     Produto,
            #     Fornecedor,
            #     Cliente,
            #     CatAPagar,
            #     CatAReceber,
            #     StatusEntrega,
            #     StatusPagamento,
            #     FormaPagamento,
            #     Compra,
            #     Venda,
            #     RelacaoCompra,
            #     RelacaoVenda,
            #     ContaAPagar,
            #     ContaAReceber,
            #     Empresa
            # ])
            conecta = Conexao()
            conecta.conecta()
            conecta.dbhandler.close_all()
            print("model")

            with conecta.dbhandler.connection_context():
                conecta.dbhandler.create_tables(models)
            """ Inserido valores padrão """

            # # Categoria a pagar
            # CatAPagar.get_or_create(categoria_a_pagar='Compra')

            # # Categoria a receber
            # CatAReceber.get_or_create(categoria_a_receber='Venda')

            # # Forma de Pagamento
            # FormaPagamento.get_or_create(forma_pagamento='Dinheiro')
            # FormaPagamento.get_or_create(forma_pagamento='Cartão')

            # # Status Entrega
            # StatusEntrega.get_or_create(status_entrega='Concluída')
            # StatusEntrega.get_or_create(status_entrega='Pendente')

            # # Status Pagamento
            # StatusPagamento.get_or_create(status_pagamento='Concluído')
            # StatusPagamento.get_or_create(status_pagamento='Pendente')

        except InternalError as err:
            print(err)


# try:
#     conecta = Conexao()
#     conecta.conecta()
#     conecta.dbhandler.connect()

# except:
#     conecta = CreateDb()
#     conecta.createDB()
#     tabelas = CriarTabelas()
#     tabelas.tabelas()

# # tabelas = CriarTabelas()

# # tabelas.tabelas()
