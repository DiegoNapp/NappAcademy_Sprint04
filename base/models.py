from pydantic import BaseModel, validator
from datetime import datetime
from useful.utils_datetime import normalize_datetime as ndt
from re import sub


class Atleta(BaseModel):
    nome: str
    cpf: str
    data_nascimento: datetime

    @validator("nome")
    def normalizar_nome(cls, v: str):
        nomes = v.split(' ')
        nome_final=[]
        for nome in nomes:
            nome_final.append(nome.capitalize())
        return ' '.join(nome_final)

    @validator("cpf")
    def normalizar_cpf(cls, v):
        v = sub('[^0-9]', '', v)
        return v

    @validator("data_nascimento", pre=True)
    def normalize_datetime(cls, v):
        v = ndt(v, format=False)
        return v

    class Config:
        orm_mode = True

class Inscricao(BaseModel):
    data_inscricao: datetime = ndt(format=False)
    id_evento: int
    id_atleta: int
    id_categoria: int
    tamanho_camiseta: str
    valor_pagar: float = 0
    valor_pago: float = 0
    valor_troco: float = 0

    @validator("tamanho_camiseta")
    def normalizar_tamanho_camiseta(cls, v: str):
        v = v.upper()
        return v

    @validator("data_inscricao", pre=True)
    def normalize_datetime(cls, v):
        v = ndt(v, format=False)
        return v

    class Config:
        orm_mode = True

class Evento(BaseModel):
    nome_evento: str
    data_realizacao: datetime
    cep: str
    endereco: str
    bairro: str
    cidade: str
    estado: str

    @validator("data_realizacao", pre=True)
    def normalize_datetime(cls, v):
        v = ndt(v, format=False)
        return v

    @validator("cep")
    def normalizar_cep(cls, v):
        v = sub('[^0-9]', '', v)
        return v

    class Config:
        orm_mode = True

class Categoria(BaseModel):
    categoria: str
    descricao: str
    distancia: float

    @validator("categoria")
    def normalizar_categoria(cls, v: str):
        v = v.upper()
        return v

    class Config:
        orm_mode = True

