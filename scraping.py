from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from datetime import datetime, timedelta
import json
from config import urlRU

semCardapio = False

def acesso_site():
    global semCardapio
    # Obtenha a data atual
    data_atual = datetime.now()

    # Verifique se a data atual é um sábado (5) ou domingo (6)
    # Se for, subtrai um dia para obter a última sexta-feira (4)
    if data_atual.weekday() == 5:  # Sábado
        data_atual -= timedelta(days=1)
    elif data_atual.weekday() == 6:  # Domingo
        data_atual -= timedelta(days=2)
    
    option = Options()
    option.add_argument('-headless') 
    driver = webdriver.Firefox(options=option)
    driver.get(urlRU)
    
    # Aguarde o carregamento dinâmico
    driver.implicitly_wait(10)  # Espera até 10 segundos

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tabela_almoco = soup.find('table', class_='refeicao almoco')
    tabela_jantar = soup.find('table', class_='refeicao jantar')
    
    if tabela_almoco is not None or tabela_jantar is not None:
        semCardapio = False
        driver.quit()
        return tabela_almoco, tabela_jantar
    else:
        semCardapio = True
        driver.quit()
        return None, None

    
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
        descricao = "" 

        for item in itens:
            if str(item).startswith('('):
                # Se o item contém uma descrição entre parênteses, armazene-o na variável 'descricao'
                descricao = item
            else:
                # Se não contém descrição, adicione o item atual e a descrição (se houver) ao JSON formatado
                json_formatado[categoria].append(item + " " + descricao)

    return json_formatado

def montar_mensagem(refeicao='almoco'):
    mensagem_cardapio = ""
    if semCardapio:
        mensagem_cardapio = "Lamento, não consegui acessar o cardápio de hoje ou este não foi publicado 😔"
        return mensagem_cardapio
    else:

        with open(f'cardapios/{refeicao}.json', 'r', encoding='utf-8') as arquivo_json:
            dados_cardapio = json.load(arquivo_json)

        if dados_cardapio:
            if refeicao == 'almoco':
                mensagem_cardapio = f"""
    🍽️ Bom dia alunos! Hoje ({dados_cardapio['DataScraping']}) no cardápio do almoço teremos: 🕛

    Prato Principal:
    - {dados_cardapio['Principal'][0]} 🍛
    - {dados_cardapio['Principal'][1]} 🍲

    Opção Vegetariana:
    - {dados_cardapio['Vegetariano'][0]} 🌱

    Acompanhamentos:
    - {dados_cardapio['Acompanhamento'][0]} 🍚
    - {dados_cardapio['Acompanhamento'][1]} 🍚
    - {dados_cardapio['Acompanhamento'][2]} 🍚
    
    Salada:
    - {dados_cardapio['Salada'][0]} 🥗
    
    Guarnição:
    - {dados_cardapio['Guarnição'][0]} 🍟

    Sobremesa:
    - {dados_cardapio['Sobremesa'][0]} 🍈
    - {dados_cardapio['Sobremesa'][1]} 🍬

    Suco:
    - {dados_cardapio['Suco'][0]} 🍹

    Atenção, tenha cuidado com alérgenos, confira os ingredientes dos pratos.
    Aproveite a sua refeição e bom apetite! 😊
    
    E aí? JaBOT Al Mossar?
    """
            else:
                mensagem_cardapio = f"""
    🍽️ Boa tarde alunos! Hoje ({dados_cardapio['DataScraping']}) no cardápio do jantar teremos: 🕕

    Prato Principal:
    - {dados_cardapio['Principal'][0]} 🍛
    - {dados_cardapio['Principal'][1]} 🍲

    Opção Vegetariana:
    - {dados_cardapio['Vegetariano'][0]} 🌱

    Acompanhamentos:
    - {dados_cardapio['Acompanhamento'][0]} 🍚
    - {dados_cardapio['Acompanhamento'][1]} 🍚
    - {dados_cardapio['Acompanhamento'][2]} 🍚
    
    Salada:
    - {dados_cardapio['Salada'][0]} 🥗
    
    Guarnição:
    - {dados_cardapio['Guarnição'][0]} 🍟

    Sobremesa:
    - {dados_cardapio['Sobremesa'][0]} 🍈
    - {dados_cardapio['Sobremesa'][1]} 🍬

    Suco:
    - {dados_cardapio['Suco'][0]} 🍹

    Atenção, tenha cuidado com alérgenos, confira os ingredientes dos pratos
    Aproveite a sua refeição e bom apetite! 😊
    
    E aí? JaBOT Al Mossar?
    """

        return mensagem_cardapio

def setup_scraping(refeicao='almoco'):
    if refeicao not in ['almoco', 'jantar']:
        raise ValueError("Refeição deve ser 'almoco' ou 'jantar'")

    tabela_almoco, tabela_jantar = acesso_site()
    
    if tabela_almoco is not None or tabela_jantar is not None:
        if refeicao == 'almoco':
            cardapio = para_json(tabela_almoco)
            arquivo_nome = 'cardapios/almoco.json'
        else:
            cardapio = para_json(tabela_jantar)
            arquivo_nome = 'cardapios/jantar.json'

        cardapio['DataScraping'] = datetime.now().strftime('%d/%m/%y')

        with open(arquivo_nome, 'w', encoding='utf-8') as arquivo:
            json.dump(cardapio, arquivo, indent=4, ensure_ascii=False)

