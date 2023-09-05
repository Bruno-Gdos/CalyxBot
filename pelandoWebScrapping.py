from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

URL = 'https://www.pelando.com.br/'
MODAL_CLASS = 'sc-dPWrhe'
SHOP_NAME_CLASS = 'sc-lbVpMG'
NAME_AND_LINK_CLASS = 'sc-khsqcC'
PRICE_CLASS = 'sc-iAEawV'
TEMPERATURE_CLASS = 'sc-hOzowv'
SWITCH_CLASS = 'sc-PBEJI'

async def get_promocao(model_pelando = 'q'):
    if model_pelando == 'r':
        newUrl = URL + 'recentes'
    elif model_pelando == 'q':
        newUrl = URL + 'mais-quentes'

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Não abra o navegador
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=options)
    driver.get(newUrl)
    time.sleep(0.5)

    # Defina um contador para o número de vezes que você deseja rolar a página
    #CLICAR NO SWITCH
    switch = driver.find_element(By.CLASS_NAME, SWITCH_CLASS)
    switch.click()
    time.sleep(1)
    # Agora que a página foi totalmente carregada, você pode coletar os dados com o BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    modal_promocoes = soup.find_all(class_= MODAL_CLASS, limit= 10)
    promocoes = []
    for modal in modal_promocoes:
        try:
            shop_name = modal.find(class_ = SHOP_NAME_CLASS).text
        except:
            shop_name = 'Não informado'
        name_and_link = modal.find(class_ = NAME_AND_LINK_CLASS)
        #name tem um atributo title com o titulo
        name = name_and_link.text
        link = URL + name_and_link['href']
        price = modal.find(class_ = PRICE_CLASS).text
        temperature = modal.find(class_ = TEMPERATURE_CLASS).text
        promocoes.append([shop_name, name, link, price, temperature])

    driver.quit()

   #Cria um arquivo txt com o nome promocoes + o tempo atual

    if model_pelando == 'r':
        text_aux = 'recentes'
    elif model_pelando == 'q':
        text_aux = 'quentes'
    text = f'**Promoções mais {text_aux} do Pelando **\n'
    count = 1
    for promocao in promocoes:
        text += f'**Promoção {count}**\n'
        text += f'Loja: {promocao[0]}\n'
        text += f'Nome: {promocao[1]}\n'
        text += f'Link: {promocao[2]}\n'
        text += f'Preço: {promocao[3]}\n'
        text += f'Temperatura: {promocao[4]}\n'
        text += '\n'
        count += 1

    return text


if __name__ == "__main__":
    print(get_promocao('q'))
    





    