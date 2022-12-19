import base.schemas as schemas
import base.models as models
from sqlalchemy.orm import Session
from datetime import datetime
from useful.utils_datetime import normalize_datetime as ndt
from re import sub

# Consultas
def get_atleta_cpf(db: Session, cpf: str):
    atleta = db.query(schemas.Atleta.id_atleta).filter(schemas.Atleta.cpf == sub('[^0-9]', '', cpf)).all()
    return atleta

def get_inscricao_atleta_evento(db: Session, id_atleta: int, id_evento: int):
    inscricao = db.query(schemas.Inscricao.id_inscricao).filter(schemas.Inscricao.id_atleta == id_atleta and schemas.Inscricao.id_evento == id_evento).all()
    return inscricao

def get_evento_nome_data_cep(db: Session, nome_evento: str, data_realizacao: datetime, cep: str):
    evento = db.query(schemas.Evento.id_evento).filter(schemas.Evento.nome_evento == nome_evento and schemas.Evento.data_realizacao == ndt(data_realizacao, format=False) and schemas.Evento.cep == sub('[^0-9]', '', cep)).all()
    return evento

def get_categoria_nome_distancia(db: Session, categoria: str, distancia: float):
    categoria = db.query(schemas.Categoria.id_categoria).filter(schemas.Categoria.categoria == categoria.upper() and schemas.Categoria.distancia == distancia).all()
    return categoria

# Geradores
def numero_inscricao(db: Session, id_evento: int):
    ultimo_numero = db.execute(f'SELECT MAX(numero_inscricao) FROM inscricao WHERE id_evento = {id_evento}').first()[0]
    if ultimo_numero is None:
        ultimo_numero = 1
    else:
        ultimo_numero += 1
    return ultimo_numero

# Verificadores
def varify_payment(db: Session, id_inscricao: int):
    troco = db.execute(f'SELECT valor_pago - valor_pagar FROM inscricao WHERE id_inscricao = {id_inscricao}').first()[0]
    pago = False
    if troco >= 0:
        pago = True
    return pago

# Criacoes
def create_atleta(db: Session, atleta: models.Atleta):
    if get_atleta_cpf(db, atleta.cpf) == []:
        dados_atleta =  schemas.Atleta(**atleta.dict())
        db.add(dados_atleta)
        db.commit()

def create_inscricao(db: Session, inscricao: models.Inscricao):
    if get_inscricao_atleta_evento(db, inscricao.id_atleta, inscricao.id_evento) == []:
        numero = numero_inscricao(db, inscricao.id_evento)
        dados_inscricao = schemas.Inscricao(**inscricao.dict(), numero_inscricao=numero)
        db.add(dados_inscricao)
        db.commit()

def create_evento(db: Session, evento: models.Evento):
    if get_evento_nome_data_cep(db, evento.nome_evento, evento.data_realizacao, evento.cep) == []:
        dados_evento = schemas.Evento(**evento.dict())
        db.add(dados_evento)
        db.commit()

def create_categoria(db: Session, categoria: models.Categoria):
    if get_categoria_nome_distancia(db, categoria.categoria, categoria.distancia) == []:
        dados_categoria = schemas.Categoria(**categoria.dict())
        db.add(dados_categoria)
        db.commit()

#Atualizadores
def pagar(db: Session, id_inscricao: int, valor: float):
    pago = varify_payment(db, id_inscricao)
    if pago is False:
        db.query(schemas.Inscricao).filter(schemas.Inscricao.id_inscricao == id_inscricao).update({schemas.Inscricao.valor_pago: schemas.Inscricao.valor_pago + valor, schemas.Inscricao.valor_troco: schemas.Inscricao.valor_pago + valor - schemas.Inscricao.valor_pagar})
        db.commit()

def alterar_tamanho_camiseta(db: Session, id_inscricao: int, novo_tamanho: str):
    db.query(schemas.Inscricao).filter(schemas.Inscricao.id_inscricao == id_inscricao).update({schemas.Inscricao.tamanho_camiseta: novo_tamanho.upper()})
    db.commit()

def alterar_categoria(db: Session, id_inscricao: int, novo_id_categoria: int):
    db.query(schemas.Inscricao).filter(schemas.Inscricao.id_inscricao == id_inscricao).update({schemas.Inscricao.id_categoria: novo_id_categoria})
    db.commit()


#Listagens
def quantidade_atletas_categoria(db: Session, id_evento: int, id_categoria: int = None):
    if id_categoria is None:
        listagem = db.execute(f'SELECT MAX(id_categoria), COUNT(DISTINCT(id_categoria)) FROM inscricao WHERE id_evento = {id_evento} GROUP BY id_categoria').fetchall()
    else:
        listagem = db.execute(f'SELECT MAX(id_categoria), COUNT(DISTINCT(id_categoria)) FROM inscricao WHERE id_evento = {id_evento} AND id_categoria = {id_categoria} GROUP BY id_categoria').fetchall()
    return listagem

def quantidades_camisetas_pagas(db: Session, id_evento: int, tamanho_camiseta: int = None):
    if tamanho_camiseta is None:
        quantidades = db.execute(f'SELECT MAX(tamanho_camiseta), COUNT(DISTINCT(tamanho_camiseta)) FROM inscricao WHERE id_evento = {id_evento} AND (valor_pagar - valor_pago) <= 0 GROUP BY tamanho_camiseta').fetchall()
    else:
        quantidades = db.execute(f'SELECT MAX(tamanho_camiseta), COUNT(DISTINCT(tamanho_camiseta)) FROM inscricao WHERE id_evento = {id_evento} AND tamanho_camiseta = {tamanho_camiseta} AND (valor_pagar - valor_pago) <= 0 GROUP BY tamanho_camiseta').fetchall()
    return quantidades

