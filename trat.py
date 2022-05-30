from datetime import datetime, timedelta
import json

from numpy import unicode_
from scraping import Bot
import pandas as pd
import re
from dateutil.relativedelta import relativedelta




def limpadados(dados):

    df = pd.DataFrame(dados)

        
    for linha in dados:
        k = linha.keys()
        if 'candidatos' in k:      
            linha['candidatos'] = string_int(linha['candidatos'])
        else:
            linha['candidatos'] = pd.NA

        if 'atividade' in k:
            linha['status_atual'] = linha['atividade'][0][0]
            linha['status_data'] = data_format(linha['atividade'][0][1])
        else:
            linha['atividade'] = pd.NA

        if 'data_publicacao' in k:
            linha['data_publicacao'] = data_format(linha['data_publicacao'])
        else:
            linha['data_publicacao'] = pd.NA
        
        if 'detalhes' in k:
            linha.update(xplode_detalhes(linha['detalhes']))
            linha.pop('detalhes')


def data_format(data):

    data_int = string_int(data)
    hj = datetime.today()

    if 'dia' in data:
        data_delta = relativedelta(days=data_int)
        return hj - data_delta

    elif 'semana' in data:
        data_delta = relativedelta(weeks=data_int)
        return hj - data_delta

    elif 'mes' in data:
        data_delta = relativedelta(months=data_int)
        return hj - data_delta


def xplode_detalhes(detalhes):
    
    dict_res = {'tipo_horario': detalhes[0]}
    if len(detalhes) > 1:
        if detalhes[1]:
            dict_res['nivel_cargo'] = detalhes[1].strip()
    if len(detalhes) > 2:
        if detalhes[2]:
            dict_res['qnt_funcionarios'] = string_int(detalhes[2])
    if len(detalhes) > 3:
        if detalhes[3]:
            dict_res['servico_empresa'] = detalhes[3].strip()
    if len(detalhes) > 4:
        for fora in detalhes[4:]:
            if not fora:
                continue
            elif 'conex' in fora:
                dict_res['conexoes'] = string_int(fora)
            elif 'ex-estudantes' in fora:
                dict_res['conexao_ensino'] = string_int(fora)
            elif 'corresponde' in fora:
                dict_res['perfil_corresponde'] = True
            elif 'Recrutando agora' in fora:
                dict_res['recrutando_agora'] = True
            elif 'selo de competência' in fora:
                dict_res['selo_de_competência'] = True    
    return dict_res
        
        
def string_int(string):
    numeros = re.findall('\d+', string)
    if len(numeros) == 1:
        return int(numeros[0])
    else:
        return f'{numeros[0]}-{numeros[1]}'



if __name__ == '__main__':
    
    # bot = Bot()
    # bot.minhasvagas()
    with open('data.json', 'rb') as f:
        dados = json.loads(f.read())
    limpadados(dados)
    
    
 





'7'