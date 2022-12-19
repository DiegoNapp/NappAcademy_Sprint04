from base.database import SessionLocal, engine
import base.schemas as schemas
import base.models as models
import base.crud as crud
import os


class ApresentacaoSprint04:
    def __init__(self):
        if os.path.exists('./EventosCorridas.db'):
            os.remove('./EventosCorridas.db')
        schemas.Base.metadata.create_all(bind=engine)
        self.session = SessionLocal() 

    def __del__(self):
        print('Close Data Base')
        self.session.close()

    def gerar_categorias(self):
        categorias = [
            models.Categoria(
                categoria='Kids',
                descricao='Somente crianças até dez anos. Corrida de 100 metros.',
                distancia=100
            ),
            models.Categoria(
                categoria='Caminhada 5K',
                descricao='Somente atletas que não querem correr, apenas caminhar 5 km.',
                distancia=5000
            ),
            models.Categoria(
                categoria='Corrida 5K',
                descricao='Corredores com um pulmão normal que corre 5 km.',
                distancia=5000
            ),
            models.Categoria(
                categoria='Corrida 10K',
                descricao='Corredores com um pulmão treinado que corre 10 km.',
                distancia=10000
            ),
            models.Categoria(
                categoria='Corrida 21K',
                descricao='Corredores com um pulmão que o prof Orlando nunca terá, o pessoal de 21 km.',
                distancia=21000
            )
        ]
        for categoria in categorias:
            crud.create_categoria(self.session, categoria)

    def gerar_evento(self):
        evento = models.Evento(
            nome_evento='São Silvestre NappAcademy 2022',
            data_realizacao='2022-12-22',
            cep='13613000',
            endereco='Avenida da Saudade, 189',
            bairro='Jardim Nova Leme',
            cidade='Leme',
            estado='SP'
        )
        crud.create_evento(self.session, evento)

    def gerar_atletas(self):
        atletas = [
            models.Atleta(
                nome='Diego Pires',
                cpf='987.654.345-29',
                data_nascimento='12-12-2001'
            ),
            models.Atleta(
                nome='Mateus Rodrigues',
                cpf='48964267391',
                data_nascimento='2001-04-23'
            ),
            models.Atleta(
                nome='Igor',
                cpf='23709476524',
                data_nascimento='04/03/2014'
            )
        ]
        for atleta in atletas:
            crud.create_atleta(self.session, atleta)

    def inscrever_atletas(self):
        id_evento = 1
        inscricoes = [
            models.Inscricao(
                id_evento=id_evento,
                id_atleta=1,
                id_categoria=5,
                tamanho_camiseta='M',
                valor_pagar=40
            ),
            models.Inscricao(
                id_evento=id_evento,
                id_atleta=2,
                id_categoria=2,
                tamanho_camiseta='GG',
                valor_pagar=60
            ),
            models.Inscricao(
                id_evento=id_evento,
                id_atleta=3,
                id_categoria=1,
                tamanho_camiseta='P',
                valor_pagar=30
            )
        ]
        for inscricao in inscricoes:
            crud.create_inscricao(self.session, inscricao)

    def consultar_id_atleta(self, cpf='987.654.345-29'):
        atleta = crud.get_atleta_cpf(self.session, cpf)
        if atleta == []:
            id_atleta = 'Atleta não cadastrado'
        else:
            id_atleta = atleta[0][0]
        return id_atleta

    def consultar_id_inscricao(self, id_atleta=1, id_evento=1):
        inscricao = crud.get_inscricao_atleta_evento(self.session, id_atleta, id_evento)
        if inscricao == []:
            id_inscricao = 'Atleta não inscrito paar este evento'
        else:
            id_inscricao = inscricao[0][0]
        return id_inscricao

    def consultar_id_evento(self, nome='São Silvestre NappAcademy 2022', data='2022-12-22', cep='13613000'):
        evento = crud.get_evento_nome_data_cep(self.session, nome, data, cep)
        if evento == []:
            id_evento = 'Evento não encontrado'
        else:
            id_evento = evento[0][0]
        return id_evento

    def consultar_id_categoria(self, nome='Corrida 5K', distancia=5000):
        categoria = crud.get_categoria_nome_distancia(self.session, nome, distancia)
        if categoria == []:
            id_categoria = 'Categoria não encontrada'
        else:
            id_categoria = categoria[0][0]
        return id_categoria

    def pagar_kit(self, id_inscricao=1, valor_pagar=40.00):
        crud.pagar(self.session, id_inscricao, valor_pagar)

    def alterar_tamanho_camiseta_inscricao(self, id_inscricao=1, novo_tamanho='P'):
        crud.alterar_tamanho_camiseta(self.session, id_inscricao, novo_tamanho)

    def alterar_categoria_inscricao(self, id_inscricao=1, novo_id_categoria=2):
        crud.alterar_categoria(self.session, id_inscricao, novo_id_categoria)

    def listar_quantidade_atletas_por_categoria(self, id_evento=1, id_categoria=None):
        listagem = []
        listagem = crud.quantidade_atletas_categoria(self.session, id_evento, id_categoria)
        print(listagem)

    def listar_quantidade_camisetas_pagas_por_tamanho(self, id_evento=1, tamanho_camiseta=None):
        listagem = []
        listagem = crud.quantidades_camisetas_pagas(self.session, id_evento, tamanho_camiseta)
        print(listagem)

client = ApresentacaoSprint04()
client.gerar_categorias()
client.gerar_evento()
client.gerar_atletas()
client.inscrever_atletas()

