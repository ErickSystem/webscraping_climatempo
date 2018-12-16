import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs

DRIVE_CHROME = os.getcwd() + '/drives/chromedriver'
URL = 'https://www.climatempo.com.br'
URL_STATE = f'{URL}/climatologia/6/riobranco-ac'
COLUMNS = ['estado', 'cidade', 'cidade_nome', 'mes', 'minima',
             'maxima', 'precipitacao', 'link'
]

def get_wait(url, driver, sleep, xpath='//*[@id="_cm-css-reset"]', video=True):
    '''

    '''
    wait = WebDriverWait(driver, sleep)
    driver.get(url)
    clima_tempo = wait.until(EC.presence_of_element_located((By.XPATH, xpath))) # elemento de video que atrapalha no load da página
    if video:
        driver.execute_script("window.stop();")  
    return clima_tempo

def create_csv(dados):
    '''

    '''
    diretorio = os.getcwd() + '/csv/'
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    
    now = datetime.now()
    arquivo = 'climatempo_' + datetime.strftime(now, '%Y-%m-%d_%H:%M') + '.csv'
    arquivo = os.path.join(diretorio, arquivo)
    df = pd.DataFrame(dados, columns=COLUMNS)
    df = df.sort_values(['estado', 'cidade_nome'], ascending=True)
    df.to_csv(arquivo, encoding='UTF-8', index=False)

def get_states_citys(options_state, driver):
    '''

    '''
    states_with_citys = []
    count_states = 1

    print('### OBTENDO DADOS DE ESTADOS E CIDADES ###')
    # são 26 estados (conforme wikipédia: https://pt.wikipedia.org/wiki/Lista_de_estados_brasileiros_por_n%C3%BAmero_de_munic%C3%ADpios),
    # a cada consulta terá o tempo de 5 segundos para carregar as cidades de cada estado.
    # estimativa: 26 * 5 = 130 segundos
    print('### TEMPO ESTIMADO DA CONSULTA: 2 minutos e 10 segundos ###')
    try:
        for option_state in options_state:
            # Obtendo o html options com os novos dados
            select = Select(driver.find_element_by_id('sel-state-geo'))
            if option_state.get('value') != '0':
                select.select_by_value(option_state.get('value'))
                # ao selecionar o novo estado, aguardo 5 segundos para que
                # todos as cidades sejam carregadas no segundo select
                time.sleep(5)
            
            element = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sel-city-geo"]')))
            html = element.get_attribute('innerHTML')
            bs4 = bs(html, 'html.parser')
            options_city_value = bs4.find_all('option')

            for option_city in options_city_value:
                # esta condicional é para selecionar apenas 4 cidades 
                # de cada estado
                if count_states > 4:
                    break

                states_with_citys.append({
                    'state': option_state.get('value'),
                    'city': option_city.get('value'),
                    'city_name': option_city.text
                })

                count_states = count_states + 1
            
            count_states = 1
    except Exception as e:
        print('houve algum problema para carregar os estados e cidades | ', e)
        pass

    print('## CIDADES E ESTADOS CARREGADOS COM SUCESSO! ##')
    return states_with_citys

def main():
    '''

    '''
    inicio = time.time()

    # carregando drive
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(executable_path=DRIVE_CHROME, desired_capabilities=capa)
    # carregando página inicial e parando o load ao encontrar a tag de video.
    clima_tempo = get_wait(URL_STATE, driver, 120)

    clima_tempo = (
             WebDriverWait(driver, 120)
             .until(EC.presence_of_element_located((By.XPATH, '//*[@id="mega-destaque"]/div[2]/div[1]/div[1]/p[1]/span[1]'))).click()
    )
    element = (WebDriverWait(driver, 120)
             .until(EC.presence_of_element_located((By.XPATH, '//*[@id="sel-state-geo"]')))
    )
    html = element.get_attribute('innerHTML')
    bs4 = bs(html, 'html.parser')
    options_state = bs4.find_all('option')
    
    data_table = []
    states_citys = get_states_citys(options_state, driver)
    execucao = 1
    for s in states_citys:
        progresso = round((execucao * 100) / len(states_citys), 2)
        link = None
        if s['state'] != '0':
            link = '{0}/climatologia/{1}/{2}'.format(URL, s['city'], str(s['state']).lower())
            print('Total de cidades {0} | progresso: {1}%'.format(len(states_citys), progresso))
            print('consultando link: {0}'.format(link))
        
        if link:
            try:
                driver.get(link)
                # aguarda 2 segundos para a página carregar
                time.sleep(2)
                # este elemento vai receber a tabela que contem os dados:
                # mes, minima, maxima e precipitacao
                element = (
                    WebDriverWait(driver, 120)
                        .until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="mega-destaque"]/div[2]/div[1]/div[1]/div[3]'))
                        )
                )
            except:
                continue
            else:
                html = element.get_attribute('innerHTML')
                bs4 = bs(html, 'html.parser')
                table = bs4.select_one('table')
                # este loop ira percorrer os elementos da tabela
                # e montar um dicionario com os dados
                for row in table.find_all("tr"):
                    values = dict()
                    cells = row.find_all("td")
                    if len(cells) == 4:
                        values['estado'] = s['state']
                        values['cidade'] = s['city']
                        values['cidade_nome'] = s['city_name']
                        values['mes'] = cells[0].find(text=True)
                        values['minima'] = cells[1].find(text=True)
                        values['maxima'] = cells[2].find(text=True)
                        values['precipitacao'] = cells[3].find(text=True)
                        values['link'] = link
                        data_table.append(values)

        execucao = execucao + 1

    # ao final de toda execução, o programa vai receber os dados armazenandos
    # na lista, e criar um arquivo csv.
    create_csv(data_table)

    # Fechadno o Chrome.
    driver.quit()

    fim = time.time()
    print('\n\n ##TEMPO TOTAL DE EXECUCAO %.2f ms ##' % (fim - inicio))

if __name__ == "__main__":
    try:
        main()
    except:
        print('Stop by failure')