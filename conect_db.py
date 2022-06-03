
import pandas as pd
import sqlalchemy as db
from sqlalchemy.sql import select

# import psycopg2 as psy
import os
from dotenv import load_dotenv
env = load_dotenv('.env')

class DBConn:

    '''
    Conexão com banco de dados
    referenciado para PostgreSQL
    '''

    def __init__(self):

        '''
        parametros utilizados para criação da classe de conexão com Banco de dados
        ver parametros em .env
        '''

        self.server = 'postgresql'
        self.user = os.getenv('postgre_user')
        self.password = os.getenv('postgre_senha')
        self.host = 'localhost'
        self.db_name = os.getenv('database_name')

        self.eng = db.create_engine(f'postgresql://{self.user}:{self.password}@localhost/{self.db_name}')
        self.conn = self.eng.connect()


    def to_db(self, df, nome_tabela):
        t = self.conn.execute(f'SELECT * FROM {nome_tabela};')
        print(t)
        self.conn.execute(f'TRUNCATE {nome_tabela} RESTART IDENTITY;')
        t = self.conn.execute(f'SELECT * FROM {nome_tabela};')
        print(t)
        
        df.to_sql(nome_tabela, self.conn, if_exists='replace')
        print('FOI, FOI, SEM ERRO')
  
            
    def close(self):
        self.conn.close()
        print('BYE, BYE!!!')

        







if __name__ == '__main__':
    d = DBConn()
    f = {'atividade_vaga': pd.read_csv('./data/atividade_trat_02-06-22.csv')
          ,'vagas':  pd.read_csv('data/vagas_tratas_02-06-22.csv', sep='^')} 
    [d.to_db(df, nome) for nome, df in f.items()]

    d.close()


'7'
