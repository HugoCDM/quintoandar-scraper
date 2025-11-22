import requests
from bs4 import BeautifulSoup

choice = 'alugar'
response = requests.get('https://www.quintoandar.com.br/imovel/895179645/alugar/apartamento-1-quarto-tijuca-rio-de-janeiro')
soup = BeautifulSoup(response.content, 'html.parser')
condominium = soup.find_all('span', class_='PriceItem_buttonWrapper__j5wyB')[4]
condominium_texto = condominium.find_next('p').text.replace('R$ ', '').replace('.','')
print(condominium.text, condominium_texto)
print()