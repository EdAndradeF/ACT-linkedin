from tkinter.tix import Tree
from conect_db import DBConn
import scraping
import trat



def menu():
    print(
        '''LinkedBot:
    w : roda com janela visivel

        0 = Fim 
        1 = Auto conexao
        2 = Minhas Candidaturas DataBase
        ''')
    return input()

funcao = menu()
window = False
if funcao == 'w':
    if window:
        window = False
    else:
        window = True 
    funcao = menu()

if funcao:
    funcao = int(funcao)
    bot = scraping.Bot(window=window)
    while funcao:
        if funcao == 1:
            bot.conect()
        elif funcao == 2:
            dados = bot.minhasvagas()
            bot.bye()
            dados_trat = trat.Estructor(dados)
            conex = DBConn()
            [conex.to_db(df, nome) for nome, df in dados_trat.dfs.items()]
            conex.close()

        funcao = menu()



    
