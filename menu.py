import scraping
import trat



def menu():
    print(
        '''LinkedBot:
        0 = Fim 
        1 = Auto conexao
        2 = Minhas Candidaturas DataBase
        ''')
    return int(input())

funcao = menu()

if funcao:
    bot = scraping.Bot()
    while funcao:
        if funcao == 1:
            bot.conect()
        elif funcao ==2:
            dados = bot.minhasvagas()
            dados_trat = trat.limpadados(dados)
            


        funcao = menu()



    bot.bye()
