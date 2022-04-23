import scraping



def menu():

    print(
        '''LinkedBot:
        0 = Fim 
        1 = Auto conexao
        2 = Minhas Candidaturas DataBase
        '''
    )
    return int(input())


funcao = menu()

if funcao:
    bot = scraping.Chrome()

    while funcao:

        if funcao == 1:
            bot.conect()
        elif funcao ==2:
            bot.minhasvagas()

        funcao = menu()



    bot.bye()
