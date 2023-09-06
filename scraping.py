from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from datetime import datetime, timedelta
import json


def acesso_site():
    # Obtenha a data atual
    data_atual = datetime.now()

    # Verifique se a data atual é um sábado (5) ou domingo (6)
    # Se for, subtrai um dia para obter a última sexta-feira (4)
    if data_atual.weekday() == 5:  # Sábado
        data_atual -= timedelta(days=1)
    elif data_atual.weekday() == 6:  # Domingo
        data_atual -= timedelta(days=2)

    # Formate a data no formato 'YYYY-MM-DD'
    data_formatada = data_atual.strftime('%Y-%m-%d')
    url = 'https://www.ufc.br/restaurante/cardapio/5-restaurante-universitario-de-quixada/' + data_formatada
    
    option = Options()
    option.add_argument('-headless') 
    driver = webdriver.Firefox(options=option) #Adicionar options depois
    driver.get(url)
    
    # Aguarde o carregamento dinâmico (ajuste o tempo conforme necessário)
    driver.implicitly_wait(10)  # Espera até 10 segundos
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tabela_almoco = soup.find('table', class_='refeicao almoco')
    tabela_jantar = soup.find('table', class_='refeicao jantar')
    
    driver.quit()
    return tabela_almoco, tabela_jantar
    
def para_json(tabela):
    rows = tabela.find_all('tr', class_='item')
     
    categorias = {
        'Principal': [],
        'Vegetariano': [],
        'Salada': [],
        'Guarnição': [],
        'Acompanhamento': [],
        'Suco': [],
        'Sobremesa': []
    }
    
    for linha in rows:
        cols = linha.find_all('td')
        if cols:
            categoria = cols[0].get_text(strip=True)
            itens = []
            for col in cols[1:]:
                descs = col.find_all('span', class_='desc')
                for desc in descs:
                    itens.append(desc.get_text(strip=True))
            categorias[categoria].extend(itens)
    
    return formatar_json(categorias)

def formatar_json(json_original):
    json_formatado = {}

    for categoria, itens in json_original.items():
        json_formatado[categoria] = []
        descricao = ""  # Inicialize a descrição como uma string vazia

        for item in itens:
            if '(' in item:
                # Se o item contém uma descrição entre parênteses, armazene-o na variável 'descricao'
                descricao = item
            else:
                # Se não contém descrição, adicione o item atual e a descrição (se houver) ao JSON formatado
                json_formatado[categoria].append(item + " " + descricao)

    return json_formatado #TODO: Reprogramar essa função para concatenar as observações de alérgenos 

def montar_mensagem(refeicao='almoco'):
    with open(f'{refeicao}.json', 'r', encoding='utf-8') as arquivo_json:
        dados_cardapio = json.load(arquivo_json)
    if refeicao == 'almoco':
        mensagem_cardapio = """
🍽️ Bom dia alunos! Hoje no cardápio do almoço teremos: 🕛

Prato Principal:
- {} 🍛
- {} 🍲

Opção Vegetariana:
- {} 🌱

Acompanhamentos:
- {} 🍚
- {} 🍚
- {} 🍚

Sobremesa:
- {} 🍬
- {} 🍈

Suco:
- {} 🍹

Atenção, tenha cuidado com alérgenos, confira os ingredientes dos pratos
Aproveite a sua refeição e bom apetite! 😊
E aí? JaBOT Al Mossar?
""".format(
    dados_cardapio['Principal'][0],
    dados_cardapio['Principal'][1],
    dados_cardapio['Vegetariano'][0],
    dados_cardapio['Acompanhamento'][0],
    dados_cardapio['Acompanhamento'][1],
    dados_cardapio['Acompanhamento'][2],
    dados_cardapio['Sobremesa'][0],
    dados_cardapio['Sobremesa'][1],
    dados_cardapio['Suco'][0]
)
    else:
        mensagem_cardapio = """
🍽️ Boa tarde alunos! Hoje no cardápio do jantar teremos teremos: 🕕

Prato Principal:
- {} 🍛
- {} 🍲

Opção Vegetariana:
- {} 🌱

Acompanhamentos:
- {} 🍚
- {} 🍚
- {} 🍚

Sobremesa:
- {} 🍬
- {} 🍈

Suco:
- {} 🍹

Atenção, tenha cuidado com alérgenos, confira os ingredientes dos pratos
Aproveite a sua refeição e bom apetite! 😊
E aí? JaBOT Al Mossar?
""".format(
    dados_cardapio['Principal'][0],
    dados_cardapio['Principal'][1],
    dados_cardapio['Vegetariano'][0],
    dados_cardapio['Acompanhamento'][0],
    dados_cardapio['Acompanhamento'][1],
    dados_cardapio['Acompanhamento'][2],
    dados_cardapio['Sobremesa'][0],
    dados_cardapio['Sobremesa'][1],
    dados_cardapio['Suco'][0]
)
        
    return mensagem_cardapio

def setup_scraping(refeicao='almoco'):
    if refeicao not in ['almoco', 'jantar']:
        raise ValueError("Refeição deve ser 'almoco' ou 'jantar'")

    tabela_almoco, tabela_jantar = acesso_site()

    if refeicao == 'almoco':
        cardapio = para_json(tabela_almoco)
        arquivo_nome = 'almoco.json'
    else:
        cardapio = para_json(tabela_jantar)
        arquivo_nome = 'jantar.json'

    with open(arquivo_nome, 'w', encoding='utf-8') as arquivo:
        json.dump(cardapio, arquivo, indent=4, ensure_ascii=False)


