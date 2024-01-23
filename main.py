
# PSE FISCAL
from selenium import webdriver # 
from selenium.webdriver.common.by import By
import os 
import time
import shutil
import pandas as p

class MainFiscal:


    def __init__(self):

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


        
    def MeioPje(self):
    # ... (código anterior)

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
                time.sleep(0.1)

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

            time.sleep(3)

            # pegando as guias
            guias = self.drive.window_handles

            self.drive.close()
            time.sleep(1)  # timezin pra nao bugar

            indice_guia = 1  #
            self.drive.switch_to.window(guias[indice_guia])  # TROCANDO DE PÁGINA, TENDEU !!

            time.sleep(3)

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
              
                if os.path.exists('dados_processos.xlsx'):
                    dataf_existente = p.read_excel('dados_processos.xlsx')

                    # Adicionando novos dados ao DataFrame existente
                    dataf_concatenado = p.concat([dataf_existente, dataf], ignore_index=True)

                    # Salvando o DataFrame atualizado
                    dataf_concatenado.to_excel('dados_processos.xlsx', index=False)

                else:
                    
                    dataf.to_excel('dados_processos.xlsx', index=False)

            except Exception as e:
                print(f"houve algum erro: {e}")

                                 
        nova_url = "https://pje1g.trf3.jus.br/pje/ConsultaPublica/listView.seam"
        self.drive.get(nova_url)
        time.sleep(5)
 

    
    def FinalSaj(self):

       # falta fazer parte do cadastro.
   
    
   
cl = MainFiscal()
cl.VerificaSeExiste()
cl.Inicio()
cl.MeioPje()
cl.FinalSaj()