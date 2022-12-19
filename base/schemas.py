from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Sequence, UniqueConstraint
from base.database import Base


class Atleta(Base):
    __tablename__ = "atleta"
    id_atleta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(300))
    cpf = Column(String(14), unique=True)
    data_nascimento = Column(DateTime)

class Inscricao(Base):
    __tablename__ = "inscricao"
    id_inscricao = Column(Integer, primary_key=True, index=True, autoincrement=True)
    numero_inscricao = Column(Integer)
    data_inscricao = Column(DateTime)
    id_evento = Column(Integer, ForeignKey('evento.id_evento'), index=True)
    id_atleta = Column(Integer, ForeignKey('atleta.id_atleta'), index=True)
    id_categoria = Column(Integer, ForeignKey('categoria.id_categoria'), index=True)
    tamanho_camiseta = Column(String(4))
    valor_pagar = Column(Float)
    valor_pago = Column(Float)
    valor_troco = Column(Float)

class Evento(Base):
    __tablename__ = "evento"
    id_evento = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_evento = Column(String(300))
    data_realizacao = Column(DateTime)
    cep = Column(String(10))
    endereco = Column(String(300))
    bairro = Column(String(300))
    cidade = Column(String(200))
    estado = Column(String(200))

class Categoria(Base):
    __tablename__ = "categoria"
    id_categoria = Column(Integer, primary_key=True, index=True, autoincrement=True)
    categoria = Column(String(100))
    descricao = Column(String(300))
    distancia = Column(Float)

