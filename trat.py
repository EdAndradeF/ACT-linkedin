import json
from datetime import date
import pandas as pd
import re
from dateutil.relativedelta import relativedelta


hoje = date.today().strftime("%d-%m-%y")

class Estructor:

    atividades = {
        'Currículo baixado' : 4,
        'Candidatura visualizada' : 3,
        'Candidatura enviada' : 2,
        'Candidatou-se no site da empresa': 1
        }
    nivel = {
        'Estágio': 1,
        'Assistente': 2,
        'Júnior': 3,
        'Pleno-sênior': 4,
        'Diretor': 5,
        'Executivo': 6,
        }
    modelo = {
        'Nao-informado': 0,
        "Presencial": 1,
	    "Remoto": 2,
	    "Híbrido": 3
    }
    quantidade = {
	"nao informado": 0,
	"1 ex-funcionários da empresa": 1,
	"1-10 funcionários": 2,
	"11-50 funcionários": 3,
	"51-200 funcionários": 4,
	"201-500 funcionários": 5,
	"501-1.000 funcionários": 6,
	"1.001-5.000 funcionários": 7,
	"5.001-10.000 funcionários": 8,
	"+ de 10.001 funcionários": 9,
    }
    tipo_contratacao = {
        "Outro": 0,
        "Tempo integral": 1,
        "Meio período": 2,
        "Contrato": 3,
        "Temporário": 4,
        "Voluntário": 5,
        "Estágio": 6,
    }

    def __repr__(self) -> str:
        return 'tratador ;)'

    def __init__(self, dados):
        
        self.ativid_vaga = pd.DataFrame()
        self.vagas = self.limpadados(dados)
        self.ativid_vaga.to_csv(f'data/atividade_trat_{hoje}.csv')
  

    def limpadados(self, dados):
        
        for linha in dados:

            k = linha.keys()
            linha['id'] = int(linha['id'])

            if 'candidatos' in k:      
                linha['candidatos'] = self.string_int(linha['candidatos'])
            else:
                linha['candidatos'] = 0

            if 'local' in k:
                pass # todo splitar 
            
            if 'local_trabalho' in k:
                linha['local_trabalho'] = self.modelo[linha['local_trabalho']]
            else:
                linha['local_trabalho'] = self.modelo['Nao-informado']

            if 'data_publicacao' in k:
                linha['data_publicacao'] = self.data_format(linha['data_publicacao'])
            else:
                linha['data_publicacao'] = None
                                             
            if 'aceita_inscricao' in k:
                linha['aberta'] = 0
            else:
                linha['aberta'] = 1
                                    
            if 'atividade' in k:
                self.ativid_vaga = pd.concat([self.ativid_vaga, self.xplode_atividade(linha['atividade'], linha['id'])], ignore_index=True)
                linha.pop('atividade')
            else:
                linha['atividade'] = None

            if 'detalhes' in k:
                linha.update(self.xplode_detalhes(linha['detalhes']))
                linha.pop('detalhes')
            else:
                linha['detalhes'] = None
        df = pd.DataFrame(dados)
        df.to_csv(f'data/vagas_tratas_{hoje}.csv', sep='^')

        return df


    def xplode_detalhes(self, detalhes):
        
        dict_res = {}
        dict_res['servico'] = [x for x in detalhes if x]

        for item in detalhes:
            if not item:
                continue
            
            elif item in self.quantidade.keys():
                dict_res['quantidade_funcionario'] = self.quantidade[item]
                dict_res['servico'].remove(item)
            
            elif item in self.nivel.keys():
                dict_res['nivel_cargo'] = self.nivel[item]
                dict_res['servico'].remove(item)

            elif item in self.tipo_contratacao.keys():
                dict_res['tipo_contratacao'] = self.tipo_contratacao[item]
                dict_res['servico'].remove(item)

            elif item in self.modelo.keys():
                dict_res['local_trabalho'] = self.modelo[item]
                dict_res['servico'].remove(item)

            elif 'conex' in item:
                dict_res['conexoes'] = self.string_int(item)
                dict_res['servico'].remove(item)
            
            elif 'ex-estudantes' in item:
                dict_res['conexao_ensino'] = self.string_int(item)
                dict_res['servico'].remove(item)
        
            elif 'corresponde' in item:
                dict_res['correspondente'] = 1
                dict_res['servico'].remove(item)

            elif 'Recrutando agora' in item:
                dict_res['recrutando_agora'] = 1
                dict_res['servico'].remove(item)

            elif 'selo de competência' in item:
                dict_res['selo_competencia'] = 1 
                dict_res['servico'].remove(item)
        
        if not dict_res['servico']:
            dict_res['servico'] = 0
        
        return dict_res

        # dict_res = {'tipo_horario': detalhes[0]}
        # if len(detalhes) > 1:
        #     if detalhes[1]:
        #         dict_res['nivel_cargo'] = detalhes[1].strip()
        # if len(detalhes) > 2:
        #     if detalhes[2]:
        #         dict_res['qnt_funcionarios'] = self.string_int(detalhes[2])
        # if len(detalhes) > 3:
        #     if detalhes[3]:
        #         dict_res['servico_empresa'] = detalhes[3].strip()
        # if len(detalhes) > 4:
        #     for fora in detalhes[4:]:
        #         if not fora:
        #             continue
        #         elif 'conex' in fora:
        #             dict_res['conexoes'] = self.string_int(fora)
        #         elif 'ex-estudantes' in fora:
        #             dict_res['conexao_ensino'] = self.string_int(fora)
        #         elif 'corresponde' in fora:
        #             dict_res['perfil_corresponde'] = 1
        #         elif 'Recrutando agora' in fora:
        #             dict_res['recrutando_agora'] = 1
        #         elif 'selo de competência' in fora:
        #             dict_res['selo_de_competência'] = 1    
        # return dict_res


    def xplode_atividade(self, atividade, id):

        lis_act = []
        for act in atividade:
            dict_act = {}
            dict_act['id'] = id
            dict_act['data'] = self.data_format(act[1])
            dict_act['atividade'] = self.atividades[act[0]]
            lis_act.append(dict_act)
        df = pd.DataFrame(lis_act)
        return df

        
    def string_int(self, string):
        numeros = re.findall('\d+', string)
        if numeros:
            if len(numeros) == 1:
                return int(numeros[0])
            else:
                return f'{numeros[0]}-{numeros[1]}'


    def data_format(self, data):

        data_int = self.string_int(data)
        hj = date.today()

        if 'dia' in data:
            data_delta = hj - relativedelta(day=+data_int)
            return data_delta.strftime("%d/%m/%y")

        elif 'semana' in data:
            data_delta = hj - relativedelta(weeks=+data_int)
            return data_delta.strftime("%d/%m/%y")

        elif 'mes' in data or 'mês' in data:
            data_delta = hj - relativedelta(months=+data_int)
            return data_delta.strftime("%d/%m/%y")
             
            






if __name__ == '__main__':
    
    # bot = Bot()
    # bot.minhasvagas()
    with open('data/data.json', 'rb') as f:
        jason = json.loads(f.read())
    dados = Estructor(jason)
    print(dados)
    
    
 





'7'