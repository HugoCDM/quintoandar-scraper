# correto
from src.utils.selenium_utils import *
from src.utils.formatting import *
from src.utils.button_attempts import *
from src.utils.requests_extractor import *
from src.utils.excel_file import *
from src.config.constants import *
from src.config.colors import AnsiColors
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
from selenium.webdriver.common.keys import Keys
from time import sleep
import time 


def search_listings(
        additional: str='nao', 
        neighborhood: str='', 
        city: str='', 
        property_type: str = '', 
        property_value: str = '', 
        choice: str = '', 
        bedrooms: str='', 
        area: str='', 
        garage: str='', 
        furnished: str = '', 
        near_subway: str = '', 
        suites: str='', 
        cond_iptu: str = '', 
        floors: str='', 
        bathrooms: str='', 
        condominium_features: str ='', 
        wellness: str = '', 
        apartment_amenities: str = '', 
        furniture: str='', 
        accessibility: str='', 
        appliances: str='', 
        rooms: str='', 
        pets: str = '', 
        availability: str = ''
        ) -> None:
    
    """
    Performs automated scraping of real estate listings on QuintoAndar using Selenium and multiple
    parameter filters. After navigating through all result pages and applying dynamic filters, the 
    function extracts detailed property information using HTTP requests and BeautifulSoup, compiles 
    the data into a structured list, and generates an Excel report with formatted outputs.

    Parameters:
        additional (str): Enables additional filters (values: "sim" or "nao").
        neighborhood (str): Neighborhood or street to filter listings.
        city (str): City or state (e.g., "RJ", "Rio de Janeiro").
        property_type (str): Desired property types, accepts single or multiple values.
        property_value (str): Maximum property price for filtering.
        choice (str): Operation type: "comprar" or "alugar".
        bedrooms (str): Minimum number of bedrooms.
        area (str): Minimum usable area in square meters.
        garage (str): Minimum number of parking spaces.
        furnished (str): Whether the unit must be furnished ("sim"/"nao").
        near_subway (str): Whether the property must be near subway stations.
        suites (str): Minimum number of suites.
        cond_iptu (str): Maximum combined condominium fee + IPTU (purchase mode).
        floors (str): Minimum acceptable floor number.
        bathrooms (str): Minimum number of bathrooms.
        condominium_features (str): Comma-separated list of desired condo features.
        wellness (str): Wellness-related features (e.g., "sauna").
        apartment_amenities (str): Apartment amenities (e.g., pool, gym, playground).
        furniture (str): Required furniture items.
        accessibility (str): Accessibility-related characteristics.
        appliances (str): Home appliances required.
        rooms (str): Additional room types (e.g., office, storage).
        pets (str): Whether pets must be allowed ("sim"/"nao").
        availability (str): Desired availability like "Imediata" or "Em breve".
    """
    property_list = []
    start = time.time()

    # Função que monta o link
    link = build_link(neighborhood, city, choice)

    furnished = 'Sim' if 's' in unidecode(furnished.lower()) else 'Não' if 'n' in unidecode(furnished.lower()) else ''
    near_subway = 'Sim' if 's' in unidecode(near_subway.lower()) else 'Não' if 'n' in unidecode(near_subway.lower()) else ''
    condominium_features = unidecode_features(condominium_features)
    wellness = unidecode_features(wellness)
    apartment_amenities = unidecode_features(apartment_amenities)
    furniture = unidecode_features(furniture)
    accessibility = unidecode_features(accessibility)
    appliances = unidecode_features(appliances)
    rooms = unidecode_features(rooms)
    pets = 'Sim' if 's' in unidecode(pets.lower()) else 'Não'if 'n' in unidecode(pets.lower()) else ''
    availability = 'Imediata' if 'imediata' in unidecode(availability.lower()) else 'Em breve' if 'breve' in unidecode(availability.lower()) else ''
    neighborhood = unidecode_features(neighborhood, False)

    if property_type == 'Todos':
        property_type = ', '.join(list(PROPERTY_TYPE.values())[:-1])
    property_type = unidecode_features(property_type)

    choice = 'comprar' if 'compra' in choice.lower() else 'alugar'
    
    # Drivers config
    driver = configure_driver()
    driver.get(link)
    sleep(1)

    driver.find_element(By.CSS_SELECTOR, f'button#cockpit-open-button').click()
    sleep(.5)

    # Valor imóvel:
    property_value_field = driver.find_elements(By.CSS_SELECTOR, 'input#salePrice-input-max' if choice == 'comprar' else "input#rentPrice-input-max")[0]
    property_value_field.click()
    sleep(.1)
    property_value_field.send_keys(Keys.BACK_SPACE * 8, property_value)

    # Tipo de imóvel:
    search_more_filters(driver, property_type, 'houseTypes', True)

    # Seleção dos filtros opcionais do QuintoAndar
    if additional == 'sim':
        if choice.lower() == 'comprar':
            # Condomínio + IPTU:
            if cond_iptu:
                cond_iptu_field = driver.find_elements(By.CSS_SELECTOR, 'input#condoIptu-input-max')[0]
                cond_iptu_field.click()
                sleep(.1)
                cond_iptu_field.send_keys(Keys.BACK_SPACE * 5, cond_iptu)

        if choice.lower() == 'alugar':
            if pets:
                search_more_filters(driver, pets, 'acceptsPets')

            if availability:
                search_more_filters(driver, availability, 'availability')

        # Quartos:
        search_more_filters(driver, bedrooms, 'bedrooms')

        # Garagem:
        search_more_filters(driver, garage, 'parkingSpaces')

        # Banheiros:
        search_more_filters(driver, bathrooms, 'bathrooms')

        # Área (m²):
        if area:
            area_field = driver.find_elements(By.CSS_SELECTOR, 'input#area-input-min')[0]
            area_field.click()
            sleep(.1)
            area_field.send_keys(Keys.BACK_SPACE * 2, area)

        # Mobília:
        search_more_filters(driver, furnished, 'furnished')

        # Próximo ao metrô:
        search_more_filters(driver, near_subway, 'nearSubway')

        # Suítes:
        search_more_filters(driver, suites, 'suites')

        # Features do condomínio:
        search_more_filters(driver, condominium_features, 'installations', True)

        # Comodidades do apartamento:
        search_more_filters(driver, apartment_amenities, 'amenities', True)

        # Bem estar:
        search_more_filters(driver, wellness, 'features', True)

        # Mobílias:
        search_more_filters(driver, furniture, 'furnitures', True)

        # Acessibilidade:
        search_more_filters(driver, accessibility, 'accessibility', True)

        # Eletrodomésticos:
        search_more_filters(driver, appliances, 'appliances', True)

        # Cômodos:
        search_more_filters(driver, rooms, 'rooms', True)


    property_value_field.send_keys(Keys.TAB)
    sleep(3)
    driver.find_element(By.CSS_SELECTOR, 'button[data-testid="apply-filters-btn"]').click()
    sleep(2)

    # Vai analisar os cartões na tela
    page = 1
    print('Página atual:', page)
    while True:
        stop = False
        property_cards = driver.find_elements(By.CSS_SELECTOR, 'div.Column_column__yCK1J div a')
        for property_card in property_cards:
            address = property_card.find_elements(By.CSS_SELECTOR, 'h2.CozyTypography')[1].text.split('·') # Tem dois h2, pega o segundo
            neighborhood_apt_left = unidecode(address[0].split(',')[1].lower().strip())
            neighborhood_apt_right = unidecode(address[0].split(',')[0].lower()).strip()
            
            
            if neighborhood not in neighborhood_apt_left and neighborhood not in neighborhood_apt_right:
                stop = True
                break
                
        if stop:
            break

        button_ver_mais = button_next(driver)
        if not button_ver_mais:
            
            break
        page += 1
        print('Página atual:', page)
    
    print()
    print('-----------------------------------------------------------------------------------------')    
    print('Cliques concluídos!')
    print('Etapa de requisição para os imóveis filtrados!')
 
    for property_card in property_cards:

        address = property_card.find_elements(By.CSS_SELECTOR, 'h2.CozyTypography')[1].text.split('·') # Tem dois h2, pega o segundo
        neighborhood_apt_left = unidecode(address[0].split(',')[1].lower().strip())
        neighborhood_apt_right = unidecode(address[0].split(',')[0].lower()).strip()
        neighborhood_apt = address[0].split(',')[1]

        if neighborhood in unidecode(neighborhood_apt_left.lower()).strip() or neighborhood in neighborhood_apt_right:
            advertisement = property_card.find_element(By.CSS_SELECTOR, 'h2.CozyTypography').text # Tem dois h2, pega o primeiro, usando find_element
            link = property_card.get_attribute('href')
            price = int(property_card.find_element(By.CSS_SELECTOR, 'p.CozyTypography').text.replace('R$ ', '').replace('.', '').replace('aluguel', '').strip())
            area_apt_bedrooms = property_card.find_element(By.CSS_SELECTOR, 'h3.CozyTypography').text.split('·')
            area_apt = area_apt_bedrooms[0].replace('m²', '').strip()

            # Filtrar bedrooms a partir do que eu indiquei inicialmente ao rodar o programa
            bedrooms_apt = area_apt_bedrooms[1].replace('quartos', '').replace('quarto', '').strip()
            if bedrooms_apt.isdigit():
                bedrooms_apt = int(bedrooms_apt)
                if bedrooms and bedrooms_apt < int(bedrooms):
                    bedrooms_apt = 'ignore'
            else:
                bedrooms_apt = 'ignore'

            city = address[1].strip()
            street = address[0].split(',')[0].strip()
            # condominium = property_card.find_element(By.CSS_SELECTOR, 'div.Cozy__CardTitle-Subtitle > p').text.replace(' Condo. + IPTU', '').replace('R$ ', '').replace('total', '').strip()

            # RESPONSE
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')

            property_type_text = get_property_type(soup, property_type)
            condominium = get_condominium(soup, choice)
            iptu_month = get_iptu(soup, choice)
            iptu_year = iptu_month * 12

            if choice == 'alugar':
                fire_insurance = get_fire_insurance_service_fee(soup, 3)
                service_fee = get_fire_insurance_service_fee(soup, 4)
                total_cost = price + condominium + iptu_month + fire_insurance + service_fee 
            else:
                total_cost =  condominium + iptu_month
            
            
            
            features = property_features(soup, garage, floors, bathrooms, suites)
            all_amenities = get_amenities_list(soup)
            publication_date = get_publication_date(soup)
            all_features_condominium = get_all_condominium_features(soup)

            if choice == 'comprar':
                property_data = [advertisement, publication_date, property_type_text, street, neighborhood_apt, city,  price, area_apt, bedrooms_apt, features['suites'], features['bathrooms'], features['garage'], condominium, iptu_month, iptu_year, total_cost, features['subway'], features['floor'], features['furniture'], features['construction_year'], all_amenities, all_features_condominium, link]
            else:
                property_data = [advertisement, publication_date, property_type_text, street, neighborhood_apt, city,  price, area_apt, bedrooms_apt, features['suites'], features['bathrooms'], features['garage'], condominium, iptu_month, iptu_year, fire_insurance, service_fee, total_cost, features['pets'], features['subway'], features['floor'], features['furniture'], features['construction_year'], all_amenities, all_features_condominium, link]

            property_list.append(property_data)

    driver.close()

    if not property_list:
        print()
        print(f'{AnsiColors.RED_IGNORE_OR_ERROR}Não foi possível encontrar imóveis com os parâmetros descritos. Tente novamente!{AnsiColors.RESET}')
        return
        
    # Adiciona columns extras se foi escolhido alugar
    columns = BUY_COLUMNS if choice == 'comprar' else RENT_COLUMNS
 
    os.makedirs('files', exist_ok=True)

    df = create_excel(property_list, columns, choice, neighborhood, property_value)

    fim = time.time()

    print('-----------------------------------------------------------------------------------------')
    print(f'Quantidade de imóveis encontrados com os filtros aplicados: {AnsiColors.GREEN_FILE_SAVED}{len(df):02d}/{len(property_cards):02d}{AnsiColors.RESET}')
    print('-----------------------------------------------------------------------------------------')
    print(f'{AnsiColors.PURPLE_EXECUTION_TIME}Tempo de execução: {fim - start:.2f}s{AnsiColors.RESET}')
    
    

