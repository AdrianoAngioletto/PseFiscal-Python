from selenium import webdriver #
import re
from babel.numbers import format_currency
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
import os 
import time
import shutil
import pandas as p
from pathlib import Path
import glob


class MainFiscal:

    opcao = webdriver.ChromeOptions()  # chama classe chrome opcao, tendeu??
    opcao.add_argument("--start-maximized")  # adiciona o argumento da classe opcao bb
    drive = webdriver.Chrome(opcao)  # aqui uso a opção como argumento, ludmilo.
    # testes.
        


    def __init__(self):

         
        # self.opcao = webdriver.ChromeOptions()  # chama classe chrome opcao, tendeu??
        # self.opcao.add_argument("--start-maximized")  # adiciona o argumento da classe opcao bb
        # self.drive = webdriver.Chrome(self.opcao)  # aqui uso a opção como argumento, ludmilo.


        bemvindo_bb = '''
            +===========================================================================+
            |             BEM VINDO,  Ao Robô, PSE FISCAL FGTS                          |
            |                                                                           |
            |                                                                           |
            |          Procuradoria Geral da Fazenda 3° Regiao                          |
            |                                                                           |
            |                                                                           |    
            |                                                                           |
            | Dev:  AdrianoAngioletto                                                   |
            +===========================================================================+
            '''
        print(bemvindo_bb)


        
    def VerificaSeExiste(self):

        diretorio_atual = os.getcwd()

        lista = os.listdir(diretorio_atual)

        encontrou_xlsx = any(arquivo.endswith('.xlsx') for arquivo in lista)

        if encontrou_xlsx:

            verifica_planilhas = os.listdir()

            lista = []

    # Filtra os arquivos ocultos e mantém apenas os arquivos .xlsx
            for arquivo in verifica_planilhas:

                if os.path.isfile(arquivo) and arquivo.endswith('.xlsx'):
                    
                    lista.append(arquivo)

            for self.planilha in lista:
                novo_nome = 'processos.xlsx' # Adiciona o nome original antes do 'processo'
                
                print(f'Movendo {self.planilha} para {novo_nome}')
                
                shutil.move(self.planilha, novo_nome)

                print('Padronizando, nome da Planilha ...')

            else:
                print('Planilha processos encontrada, Carregando..')

        else:
            print('Você precisa adicionar a planilha, para Consultar, sem ela não é possivel')

            time.sleep(7)

            quit()
        
                    
    def Inicio(self):
        # PARTE PARA ABRIR O EXCEL, E CONSULTAR OS PROCESSOS

        dataf = p.read_excel(self.planilha)

        self.lista_processos = []

        numero_processo = dataf['PROCESSO TXT'].tolist()

        self.lista_processos.extend(numero_processo)

        print(f'TODOS PROCESSOS FORAM CARREGADOS!, NUMERO TOTAL DE PROCESSOS SÃO DE : {len(self.lista_processos)}')


   
    def Saj(self):

        url = 'https://saj.pgfn.fazenda.gov.br/saj/login.jsf?dswid=3754'

        self.drive.get(url) # chama o site

        time.sleep(2)

        campo_login = self.drive.find_element(By.ID, "frmLogin:username")
        campo_senha = self.drive.find_element(By.ID, "frmLogin:password")

        campo_login.send_keys("******")
        campo_senha.send_keys("mundo2024")

        botao_ok = self.drive.find_element(By.ID, "frmLogin:entrar")
        time.sleep(2)
        botao_ok.click()
        time.sleep(3)

        botao_processo = self.drive.find_element(By.CLASS_NAME, "ui-menuitem-text")  # PEGA  ID DA LISTA > PROCESS
        webdriver.ActionChains(self.drive).move_to_element(botao_processo).perform() # MOVE MOUSE ATÉ A LISTA
        time.sleep(1) # TEMPO NECESSÁRIO

        botao_consulta = self.drive.find_element(By.XPATH, '//*[@id="j_idt15:formMenus:j_idt34"]/ul/li[1]/ul/li[2]').click() # PEGA O ITEM DA LISTA >>> Processo
        time.sleep(7)

    def clica(self):

        clicando_virtual = self.drive.find_element(By. XPATH, '//*[@id="frmCadastro:tiposProcesso"]/tbody/tr/td[3]/div/div[2]').click()


        class_div = self.drive.find_element(By. XPATH, '//*[@id="frmCadastro:classe:selectOneMenu_label"]').click()

        time.sleep(2)

        opcao_class_div = self.drive.find_element(By.XPATH, "//li[text()='Execução Fiscal (FGTS e Contr. Sociais da LC 110)']").click()

        time.sleep(3)


        vara_div = self.drive.find_element(By.ID, "frmCadastro:tipoJuizo:selectOneMenu").click()

        time.sleep(2)

        opcao_vara_federal = self.drive.find_element(By.XPATH, "//li[text()='Vara Federal']").click()

        time.sleep(3)

        # agora vem o for pra pegar na "vara " :)

        time.sleep(2)


    def vara(self):

        caminho_absoluto_saj_ = Path.cwd()

        Pasta_Add_saj_ = 'Resultado_Processos'
        Processos_ = 'dados_processos.xlsx'
        Caminho_Mais_Pasta_saj_ = caminho_absoluto_saj_ / Pasta_Add_saj_

        padrao_arquivo_ = '*.xlsx' # padrão do excel
        ListaProcessos_ = glob.glob(str(Caminho_Mais_Pasta_saj_ / padrao_arquivo_))

        for caminho_do_arquivo1 in ListaProcessos_:
                    dados2 = p.read_excel(caminho_do_arquivo1)


        for vara_judicial in dados2['Vara Judicial']:

                print(f' Lendo a Vara Judicial: {vara_judicial}')

                vara_judicial = vara_judicial if not p.isna(vara_judicial) else ''

                elemento_selecao = self.drive.find_element(By.XPATH, '//*[@id="frmCadastro:juizo_input"]')
                
                elemento_selecao.click()

                elemento_selecao.send_keys(vara_judicial)

                time.sleep(2)

                pegando_numero_processo_atual = self.drive.find_element(By.XPATH, '//*[@id="frmCadastro:inNumeroProcesso:numeroProcesso"]')

                numero_processo_atual = pegando_numero_processo_atual.get_attribute('value')

                self.numero_formatado = numero_processo_atual.replace('-', '').replace('.', '')

                print("Valor na caixa de entrada:", self.numero_formatado)

                caminho_atual = Path.cwd()
                caminho_atual_excel = caminho_atual / 'processos.xlsx'

                dados_p = p.read_excel(caminho_atual_excel)

                if self.numero_formatado in dados_p['PROCESSO TXT'].values:
                    self.processo_cda = dados_p.loc[dados_p['PROCESSO TXT'] == self.numero_formatado, 'CONTRATOS'].values
                    print(f'Numero de Processo, e CDA  {self.numero_formatado}: {self.processo_cda}')
                else:
                    print(f'O número {self.numero_formatado} não foi encontrado na coluna "PROCESSO TXT".')

        
    def MeioSaj(self):
            caminho_absoluto_saj = Path.cwd()

            Pasta_Add_saj = 'Resultado_Processos'
            Processos = 'dados_processos.xlsx'
            Caminho_Mais_Pasta_saj = caminho_absoluto_saj / Pasta_Add_saj

            padrao_arquivo = '*.xlsx' # padrão do excel
            self.ListaProcessos = glob.glob(str(Caminho_Mais_Pasta_saj / padrao_arquivo))

            for self.caminho_do_arquivo1 in self.ListaProcessos:
                self.dados = p.read_excel(self.caminho_do_arquivo1)

            self.processos_iter = iter(self.dados['Numero do Processo'])

            valores_que_passaram_try = []


            for processos_planilha in self.processos_iter:
                print(f' Lendo os Processos {processos_planilha}')

        


                caixa_pesquisa = self.drive.find_element(By.XPATH, '/html/body/div[7]/div/div/span[2]/form/div[1]/div[2]/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/input')


                caixa_pesquisa.click()

                caixa_pesquisa.clear()
                time.sleep(1)

                caixa_pesquisa.send_keys(str(processos_planilha))
                time.sleep(1)

                # Clica no botão OK
                ok_botao = self.drive.find_element(By.XPATH, '//*[@id="frmPesquisaProcessoJudicial:btnOK"]').click()

                try:
                   


                    valores_que_passaram_try.append(processos_planilha)
       

                    caixa_pesquisa = self.drive.find_element(By.XPATH, '/html/body/div[7]/div/div/span[2]/form/div[1]/div[2]/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/input')
                    

                except:

                    if self.dados['Numero do Processo'].isin(valores_que_passaram_try).any():

                        # Se algum valor de valores_que_passaram_try estiver presente na coluna 'Numero do Processo'
                        # COLOQUEI -1 pq, pra sempre deixar o ultimo processo que passou, livre para não apagar o que não foi registrado.

                        indice_a_remover = self.dados[self.dados['Numero do Processo'].isin(valores_que_passaram_try[:-1])].index
                        self.dados.drop(index=indice_a_remover, inplace=True)
                        self.dados.to_excel(self.caminho_do_arquivo1, index=False)


                   
                    self.clica()
                    self.vara()



                    processo_cda_str = str(self.processo_cda[0])
                    if len(processo_cda_str) > 13:  # verifico se tem duas CDAS, se tiver, será necessário cadastrar duas vezes
                        
                        print(processo_cda_str, 'valores da CDA')

                        expressao_do_diabo_regular = re.compile(r'\b(\w+\d+)\b')
                        processo_cda_lista = expressao_do_diabo_regular.findall(processo_cda_str)

                        valor_cda1 = processo_cda_lista[0]
                        valor_cda2 = processo_cda_lista[1]

                        print(valor_cda2)

                        caixa_colocar_cda = self.drive.find_element(By.XPATH, '//*[@id="frmCadastro:inNumInscrFGTS:numInscrFGTS"]')
                        caixa_colocar_cda.click()
                        caixa_colocar_cda.send_keys(valor_cda1)

                        botao_incluir = self.drive.find_element(By.XPATH, '//*[@id="frmCadastro:btnIncluirInscrFGTS"]')
                        botao_incluir.click()

                        time.sleep(1)

                        caixa_colocar_cda = self.drive.find_element(By.XPATH, '//*[@id="frmCadastro:inNumInscrFGTS:numInscrFGTS"]')
                        caixa_colocar_cda.click()
                        caixa_colocar_cda.send_keys(valor_cda2)

                        botao_incluir = self.drive.find_element(By.XPATH, '//*[@id="frmCadastro:btnIncluirInscrFGTS"]')
                        botao_incluir.click()

                        caminho_absoluto_saj_ = Path.cwd()

                        Pasta_Add_saj_ = 'Resultado_Processos'
                        Processos_ = 'dados_processos.xlsx'
                        Caminho_Mais_Pasta_saj_ = caminho_absoluto_saj_ / Pasta_Add_saj_

                        padrao_arquivo_ = '*.xlsx' # padrão do excel
                        ListaProcessos_ = glob.glob(str(Caminho_Mais_Pasta_saj_ / padrao_arquivo_))

                        for caminho_do_arquivo1 in ListaProcessos_:
                                dados2 = p.read_excel(caminho_do_arquivo1)

                        for DataDistribuicao in dados2['Data Distribuicao']:
                            
                            data_sem_hora = DataDistribuicao
                            

                        calendario = self.drive.find_element(By.XPATH, '//*[@id="frmCadastro:dataProtocoloJustica:calendar_input"]')

                        
                        script = f"arguments[0].value = '{data_sem_hora}';"
                        self.drive.execute_script(script, calendario)


                        
                        data_frame_novo = p.read_excel(self.planilha)

                        if self.numero_formatado in data_frame_novo['PROCESSO TXT'].values:
                            self.valor_causa = data_frame_novo.loc[data_frame_novo['PROCESSO TXT'] == self.numero_formatado, 'VALOR DA CAUSA ORIGINAL'].values
                            print(f'Numero de Processo, e CDA  {self.numero_formatado}: {self.valor_causa}')
                        else:
                            print(f'O número {self.numero_formatado} não foi encontrado na coluna "PROCESSO TXT".')


                                        
                        inserir_valor_causa = self.drive.find_element(By. XPATH, '//*[@id="frmCadastro:inValorCausa:valorCausa"]')

                        print(f'{type(self.valor_causa)} VALOR >> {self.valor_causa}')

                        valor = self.valor_causa[0]

                        
                        valor_formatado = float(valor)

                        valor_formatado_dinheiro = format_currency(valor_formatado, 'BRL', locale='pt_BR')

                        print(f'{type(valor_formatado_dinheiro)} --- {valor_formatado_dinheiro}')


        
                        script = f"arguments[0].value = '{valor_formatado_dinheiro}';"
                        self.drive.execute_script(script, inserir_valor_causa)

                        time.sleep(10)


                        finalizar_salvar_processo = self.drive.find_element(By. XPATH, '//*[@id="frmCadastro:btnSalvar"]/span')

                        finalizar_salvar_processo.click()

                        time.sleep(5)


                        
                        botao_voltar = self.drive.find_element(By.XPATH, '//*[@id="frmCadastro:btnVoltar"]')
                        botao_voltar.click()


                        time.sleep(10)


                    
                    else:

                        expressao_do_diabo_regular = re.compile(r'\b(\w+\d+)\b')
                        processo_cda_lista = expressao_do_diabo_regular.findall(processo_cda_str)

                        valor_cdal = processo_cda_lista[0]

                        print(valor_cda1)

                        caixa_colocar_cda = self.drive.find_element(By.XPATH, '//*[@id="frmCadastro:inNumInscrFGTS:numInscrFGTS"]')

                        caixa_colocar_cda.click()

                        caixa_colocar_cda.send_keys(valor_cdal)

                        botao_incluir = self.drive.find_element(By.XPATH, '//*[@id="frmCadastro:btnIncluirInscrFGTS"]')


                        botao_incluir.click()

                        time.sleep(1)


                        caminho_absoluto_saj_ = Path.cwd()

                        Pasta_Add_saj_ = 'Resultado_Processos'
                        Processos_ = 'dados_processos.xlsx'
                        Caminho_Mais_Pasta_saj_ = caminho_absoluto_saj_ / Pasta_Add_saj_

                        padrao_arquivo_ = '*.xlsx' # padrão do excel
                        ListaProcessos_ = glob.glob(str(Caminho_Mais_Pasta_saj_ / padrao_arquivo_))

                        for caminho_do_arquivo1 in ListaProcessos_:
                                dados2 = p.read_excel(caminho_do_arquivo1)

                        for DataDistribuicao in dados2['Data Distribuicao']:
                            
                            data_sem_hora = DataDistribuicao
                            


                        calendario = self.drive.find_element(By.XPATH, '//*[@id="frmCadastro:dataProtocoloJustica:calendar_input"]')

                      
                        script = f"arguments[0].value = '{data_sem_hora}';"
                        self.drive.execute_script(script, calendario)


                        
                        data_frame_novo = p.read_excel(self.planilha)

                        if self.numero_formatado in data_frame_novo['PROCESSO TXT'].values:
                            self.valor_causa = data_frame_novo.loc[data_frame_novo['PROCESSO TXT'] == self.numero_formatado, 'VALOR DA CAUSA ORIGINAL'].values
                            print(f'Numero de Processo, e CDA  {self.numero_formatado}: {self.valor_causa}')
                        else:
                            print(f'O número {self.numero_formatado} não foi encontrado na coluna "PROCESSO TXT".')


                                        
                        inserir_valor_causa = self.drive.find_element(By. XPATH, '//*[@id="frmCadastro:inValorCausa:valorCausa"]')

                        print(f'{type(self.valor_causa)} VALOR >> {self.valor_causa}')

                        valor = self.valor_causa[0]

                        
                        valor_formatado = float(valor)

                        valor_formatado_dinheiro = format_currency(valor_formatado, 'BRL', locale='pt_BR')

                        print(f'{type(valor_formatado_dinheiro)} --- {valor_formatado_dinheiro}')


        
                        script = f"arguments[0].value = '{valor_formatado_dinheiro}';"
                        self.drive.execute_script(script, inserir_valor_causa)


                        finalizar_salvar_processo = self.drive.find_element(By. XPATH, '//*[@id="frmCadastro:btnSalvar"]/span')

                        finalizar_salvar_processo.click()


                        time.sleep(5)
                        


                        botao_voltar = self.drive.find_element(By.XPATH, '//*[@id="frmCadastro:btnVoltar"]')
                        botao_voltar.click()



                        

                                   
                    
    def MeioPje(self):
        Pasta_Nova = 'Resultado_Processos'

        if not os.path.exists(Pasta_Nova):
            os.makedirs(Pasta_Nova)

            print(f" Criando Pasta, {Pasta_Nova}... ")

        for numerop in self.lista_processos:
            # AQUI É A PARTE DE CONSULTAR OS PROCESSOS NO PJE, PARA SABER AS CLASSES, PRA SÓ DEPOIS FAZER A CONSULTA

            #  ACESSANDO SITE PARA CONSULTAR, O NUMERO DOS PROCESSOS
            self.opcao = webdriver.ChromeOptions()  # chama classe chrome opcao, tendeu??
            self.opcao.add_argument("--start-maximized")  # adiciona o argumento da classe opcao bb
            self.drive = webdriver.Chrome(self.opcao)  # aqui uso a opção como argumento, ludmilo.

            self.drive.get('https://pje1g.trf3.jus.br/pje/ConsultaPublica/listView.seam')

            pega_numero = self.drive.find_element(By.ID, "fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso")

            # Esse FOR é necessário, por que quem fez o pje, colocou "máscara de entrada", para dificultar o trabalho.
            for caractere in numerop:
                pega_numero.send_keys(caractere)
                

            print(f"Consultando processo: {numerop}")

            botao_consultar = self.drive.find_element(By.ID, 'fPP:searchProcessos').click()  # PRIMEIRO BOTÃO CONSULTAR, O PESQUISAR,
            
            time.sleep(5)

            try:
                
                botao_abrir_processo = self.drive.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/form/div[2]/div/table/tbody/tr/td[1]/a').click()  # SEGUNDO BOTÃO PRA ABRIR OS DADOS DO PROCESSOS
            except:
                print(f'PROCESSO NÃO ENCONTRADO NO PJE {numerop}')

                with open(f'Processos_Nao_Encontrados.txt', 'a', encoding='UTF-8') as logdoprocesso:

                    logdoprocesso.write(f'o processo: {numerop}, não foi encontrado \n ')  

                    continue


            # pegando as guias
            guias = self.drive.window_handles

            self.drive.close()
            time.sleep(1)  # timezin pra nao bugar

            indice_guia = 1  #
            self.drive.switch_to.window(guias[indice_guia])  # TROCANDO DE PÁGINA, TENDEU !!

            time.sleep(1)

            conteudo_lista = []

            Numero_do_Processo = self.drive.find_element(By.XPATH, '//*[@id="j_id131:processoTrfViewView:j_id137"]/div/div[2]/div')
            Data_Distribuicao = self.drive.find_element(By.XPATH, '//*[@id="j_id131:processoTrfViewView:j_id149"]/div/div[2]')
            # Classe_Judicial = self.drive.find_element(By.XPATH, '//*[@id="j_id131:processoTrfViewView:j_id160"]/div/div[2]') # SE CASO PRECISAR DA CLASSE JA ESTA SALVO
            Vara_Judicial = self.drive.find_element(By.XPATH, '//*[@id="j_id131:processoTrfViewView:j_id208"]/div/div[2]')


            Numero_do_Processod = Numero_do_Processo.text
            Data_Distribuicaod = Data_Distribuicao.text
            # Classe_Judiciald = Classe_Judicial.text # se precisar ja esta salvo
            Vara_Judiciald = Vara_Judicial.text

            conteudo_lista.append([Numero_do_Processod, Data_Distribuicaod, Vara_Judiciald])

            colunas = ['Numero do Processo', 'Data Distribuicao', 'Vara Judicial' ]

            dataf = p.DataFrame(conteudo_lista, columns=colunas)
            
            try:
                
                # Criando logica para pegar caminho, e adicionar + o nome da pasta :)

                caminho_absoluto = Path.cwd()

                Pasta_Add = 'Resultado_Processos'

                Caminho_Mais_Pasta = caminho_absoluto / Pasta_Add
              
                 
                nome_arquivo = 'dados_processos.xlsx'

                
                caminho_do_arquivo = Caminho_Mais_Pasta / nome_arquivo

                
                if caminho_do_arquivo.exists():
                
                    dataf_existente = p.read_excel(caminho_do_arquivo)

                  
                    dataf_concatenado = p.concat([dataf_existente, dataf], ignore_index=True)

    
                    dataf_concatenado.to_excel(caminho_do_arquivo, index=False)
                else:
                   
                    dataf.to_excel(caminho_do_arquivo, index=False)

            except Exception as e:
                print(f"Houve algum erro: {e}")

                                 
        nova_url = "https://pje1g.trf3.jus.br/pje/ConsultaPublica/listView.seam"
        self.drive.get(nova_url)
        time.sleep(3)



Cl = MainFiscal()
Cl.VerificaSeExiste()
Cl.Inicio()
Cl.Saj()
Cl.MeioSaj()
