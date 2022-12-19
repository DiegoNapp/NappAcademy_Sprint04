from base.database import SessionLocal, engine
from sqlalchemy.orm.session import Session
import base.schemas as schemas
import base.models as models
import base.crud as crud
from datetime import datetime
import os


class TestDataBase:
    def test_create_databse(self):
        if os.path.exists('./EventosCorridas.db'):
            os.remove('./EventosCorridas.db')
        assert os.path.exists('./EventosCorridas.db') == False
        schemas.Base.metadata.create_all(bind=engine)
        assert os.path.exists('./EventosCorridas.db') == True

    def test_session(self):
        session = SessionLocal()
        assert isinstance(session, Session)
        session.close()

class TestModel:
    def test_instance_model_atleta(self):
        atleta = models.Atleta(
            nome = 'diego pires',
            cpf = '657.837.987-23',
            data_nascimento = '2001-01-01'
        )
        assert isinstance(atleta, models.Atleta)
        assert isinstance(atleta.dict(), dict)
        assert len(atleta.dict().keys()) == 3
        assert atleta.nome == 'Diego Pires'
        assert atleta.cpf == '65783798723'
        assert isinstance(atleta.data_nascimento, datetime)

    def test_instance_inscricao(self):
        inscricao = models.Inscricao(
            id_evento=2,
            id_atleta=1,
            id_categoria=4,
            tamanho_camiseta='M',
            valor_pagar=50.00,
            valor_pago=60.00,
            valor_troco=10.00
        )
        assert isinstance(inscricao, models.Inscricao)
        assert isinstance(inscricao.dict(), dict)
        assert len(inscricao.dict().keys()) == 8
        assert isinstance(inscricao.data_inscricao, datetime)
        assert inscricao.data_inscricao.strftime('%Y-%m-%d %H:%M:%S') == datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def test_instance_evento(self):
        evento = models.Evento(
            nome_evento = 'São Silvestre 2022',
            data_realizacao = '2022-12-22',
            cep = '136176-21',
            endereco = 'Avenida da Saudade, 189',
            bairro = 'Jardim Nova Leme',
            cidade = 'Leme',
            estado='SP'
        )
        assert isinstance(evento, models.Evento)
        assert isinstance(evento.dict(), dict)
        assert len(evento.dict().keys()) == 7
        assert isinstance(evento.data_realizacao, datetime)

    def test_instance_categoria(self):
        categoria = models.Categoria(
            categoria = 'Caminhada 5K',
            descricao = 'Somente atletas que não querem correr, apenas caminhar 5 km.',
            distancia = 5000
        )
        assert isinstance(categoria, models.Categoria)
        assert isinstance(categoria.dict(), dict)
        assert len(categoria.dict().keys()) == 3

class TestSchemas:
    def setup_class(self):
        if os.path.exists('./EventosCorridas.db'):
            os.remove('./EventosCorridas.db')
        schemas.Base.metadata.create_all(bind=engine)
        self.session = SessionLocal()   

    def test_table_atleta(self):
        assert str(self.session.query(schemas.Atleta.id_atleta).column_descriptions[0]['type']) == 'INTEGER'
        assert str(self.session.query(schemas.Atleta.nome).column_descriptions[0]['type']) == 'VARCHAR(300)'
        assert str(self.session.query(schemas.Atleta.cpf).column_descriptions[0]['type']) == 'VARCHAR(14)'
        assert str(self.session.query(schemas.Atleta.data_nascimento).column_descriptions[0]['type']) == 'DATETIME'
        self.session.close()

    def test_table_inscricao(self):
        assert str(self.session.query(schemas.Inscricao.id_inscricao).column_descriptions[0]['type']) == 'INTEGER'
        assert str(self.session.query(schemas.Inscricao.numero_inscricao).column_descriptions[0]['type']) == 'INTEGER'
        assert str(self.session.query(schemas.Inscricao.data_inscricao).column_descriptions[0]['type']) == 'DATETIME'
        assert str(self.session.query(schemas.Inscricao.id_evento).column_descriptions[0]['type']) == 'INTEGER'
        assert str(self.session.query(schemas.Inscricao.id_atleta).column_descriptions[0]['type']) == 'INTEGER'
        assert str(self.session.query(schemas.Inscricao.id_categoria).column_descriptions[0]['type']) == 'INTEGER'
        assert str(self.session.query(schemas.Inscricao.tamanho_camiseta).column_descriptions[0]['type']) == 'VARCHAR(4)'
        self.session.close()

    def test_table_evento(self):
        assert str(self.session.query(schemas.Evento.id_evento).column_descriptions[0]['type']) == 'INTEGER'
        assert str(self.session.query(schemas.Evento.nome_evento).column_descriptions[0]['type']) == 'VARCHAR(300)'
        assert str(self.session.query(schemas.Evento.data_realizacao).column_descriptions[0]['type']) == 'DATETIME'
        assert str(self.session.query(schemas.Evento.cep).column_descriptions[0]['type']) == 'VARCHAR(10)'
        assert str(self.session.query(schemas.Evento.endereco).column_descriptions[0]['type']) == 'VARCHAR(300)'
        assert str(self.session.query(schemas.Evento.bairro).column_descriptions[0]['type']) == 'VARCHAR(300)'
        assert str(self.session.query(schemas.Evento.cidade).column_descriptions[0]['type']) == 'VARCHAR(200)'
        assert str(self.session.query(schemas.Evento.estado).column_descriptions[0]['type']) == 'VARCHAR(200)'
        self.session.close()
        
    def test_table_categoria(self):
        assert str(self.session.query(schemas.Categoria.id_categoria).column_descriptions[0]['type']) == 'INTEGER'
        assert str(self.session.query(schemas.Categoria.categoria).column_descriptions[0]['type']) == 'VARCHAR(100)'
        assert str(self.session.query(schemas.Categoria.descricao).column_descriptions[0]['type']) == 'VARCHAR(300)'
        assert str(self.session.query(schemas.Categoria.distancia).column_descriptions[0]['type']) == 'FLOAT'
        self.session.close()

class TestCrud:
    def setup_class(self):
        if os.path.exists('./EventosCorridas.db'):
            os.remove('./EventosCorridas.db')
        schemas.Base.metadata.create_all(bind=engine)
        self.session = SessionLocal()

    def test_create_atleta(self):
        atleta = models.Atleta(
            nome = 'diego pires',
            cpf = '657.837.987-23',
            data_nascimento = '2001-01-01'
        )
        crud.create_atleta(self.session, atleta)
        self.session.close()

    def test_get_atleta_cpf(self):
        atleta_valido = crud.get_atleta_cpf(self.session, '65783798723')
        atleta_invalido = crud.get_atleta_cpf(self.session, '98346723984')
        assert len(atleta_valido) == 1
        assert atleta_invalido == []
        self.session.close()

    def test_create_inscricao(self):
        inscricao = models.Inscricao(
            numero_inscricao=1,
            id_evento=2,
            id_atleta=1,
            id_categoria=4,
            tamanho_camiseta='M',
            valor_pagar=50.00,
            valor_pago=00.00,
            valor_troco=00.00
        )
        crud.create_inscricao(self.session, inscricao)
        self.session.close()

    def test_get_inscricao_atleta_evento(self):
        inscricao_valida = crud.get_inscricao_atleta_evento(self.session, 1, 2)
        inscricao_invalida = crud.get_inscricao_atleta_evento(self.session, 34, 87)
        assert len(inscricao_valida) == 1
        assert inscricao_invalida == []
        self.session.close()

    def test_numero_inscricao(self):
        proximo_numero = crud.numero_inscricao(self.session, 1)
        assert isinstance(proximo_numero, int)
        assert proximo_numero == 1 

    def test_create_evento(self):
        evento = models.Evento(
            nome_evento = 'São Silvestre 2022',
            data_realizacao = '2022-12-22',
            cep = '136176-21',
            endereco = 'Avenida da Saudade, 189',
            bairro = 'Jardim Nova Leme',
            cidade = 'Leme',
            estado='SP'
        )
        crud.create_evento(self.session, evento)
        self.session.close

    def test_get_evento_nome_data_cep(self):
        evento_valido = crud.get_evento_nome_data_cep(self.session, 'São Silvestre 2022', '2022-12-22', '136176-21')
        evento_invalido = crud.get_evento_nome_data_cep(self.session, 'Evento Inexistente', '2022-12-22', '136176-21')
        assert len(evento_valido) == 1
        assert evento_invalido == []
        self.session.close()

    def test_create_categoria(self):
        categoria = models.Categoria(
            categoria = 'Caminhada 5K',
            descricao = 'Somente atletas que não querem correr, apenas caminhar 5 km.',
            distancia = 5000
        )
        crud.create_categoria(self.session, categoria)
        self.session.close
    
    def test_get_categoria_nome_distancia(self):
        categoria_valida = crud.get_categoria_nome_distancia(self.session, 'Caminhada 5K', 5000)
        categoria_invalida = crud.get_categoria_nome_distancia(self.session, 'Categoria Inexistente', 999999)
        assert len(categoria_valida) == 1
        assert categoria_invalida == []
        self.session.close()

    def test_varify_payment(self):
        pago = crud.varify_payment(self.session, 1)
        assert isinstance(pago, bool)
        assert pago is False

    def test_pagar(self):
        crud.pagar(self.session, 1, 50)
        pago = crud.varify_payment(self.session, 1)
        assert isinstance(pago, bool)
        assert pago is True
        self.session.close()

    def test_quantidade_atletas_categoria(self):
        listagem = crud.quantidade_atletas_categoria(self.session, 2)
        assert isinstance(listagem, list)
        assert (4, 1) in listagem

    def test_quantidades_camisetas_pagas(self):
        lista_quantidades = crud.quantidades_camisetas_pagas(self.session, 2)
        assert isinstance(lista_quantidades, list)
        assert ('M', 1) in lista_quantidades
    
    def test_alterar_tamanho_camiseta(self):
        assert 'M' in self.session.query(schemas.Inscricao.tamanho_camiseta).filter(schemas.Inscricao.id_inscricao == 1).all()[0]
        crud.alterar_tamanho_camiseta(self.session, 1, 'G')
        assert 'G' in self.session.query(schemas.Inscricao.tamanho_camiseta).filter(schemas.Inscricao.id_inscricao == 1).all()[0]

    def test_alterar_categoria(self):
        assert 4 in self.session.query(schemas.Inscricao.id_categoria).filter(schemas.Inscricao.id_inscricao == 1).all()[0]
        crud.alterar_categoria(self.session, 1, 3)
        assert 3 in self.session.query(schemas.Inscricao.id_categoria).filter(schemas.Inscricao.id_inscricao == 1).all()[0]