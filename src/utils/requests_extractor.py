from src.utils.formatting import *
from src.config.constants import *
from bs4 import BeautifulSoup

def get_property_type(
        soup: BeautifulSoup, 
        property_type: str
        ) -> str:
    
    """
    Determines the property type based on the page's main heading.

    Parameters:
        soup (BeautifulSoup): Parsed HTML content of the property page.
        property_type (str): The user-selected property type filter.
    """

    h1_property_type = unidecode_features(soup.find('h1').text, False)
    mapping = dict(sorted(FORMATTED_PROPERTY_TYPE.items(), key=lambda x: -len(x[0])))
    text_property_type = next((v for k,v in mapping.items() if k in h1_property_type), 'Não informado')

    normalized_property_type = unidecode_features(text_property_type, False)

    if property_type and normalized_property_type not in property_type:
        text_property_type = 'ignore'
    return text_property_type


def get_iptu(
        soup: BeautifulSoup,
        choice: str
        ) -> int:
    
    """
    Extracts the IPTU (property tax) value from the listing page.

    Parameters:
        soup (BeautifulSoup): Parsed HTML content of the property page.
        choice (str): Indicates whether the listing is for purchase ("comprar") or rent ("alugar").
    """

    iptu = int(soup.find_all('div', class_='PriceItem_valueWrapper__lmF_y')[1].text.replace('12x R$', '').replace('.', '').strip()) if choice == 'comprar' else int(soup.find_all('span', class_='PriceItem_buttonWrapper__j5wyB')[2].find_next('p').text.replace('R$', '').replace('.', '').strip())
    return iptu    


def get_condominium(
        soup: BeautifulSoup,
        choice: str
        ) -> int:
    
    """
    Extracts the condominium fee value from the listing page.

    Parameters:
        soup (BeautifulSoup): Parsed HTML content of the property page.
        choice (str): Indicates whether the listing is for purchase ("comprar") or rent ("alugar").
    
    """
    
    condominium = int(soup.find_all('div', class_='PriceItem_valueWrapper__lmF_y')[0].text.replace('R$', '').replace('.', '').strip()) if choice == 'comprar' else int(soup.find_all('span', class_='PriceItem_buttonWrapper__j5wyB')[1].find_next('p').text.replace('R$', '').replace('.', '').strip())
    return condominium


def get_fire_insurance_service_fee(soup, insurance_or_service_fee):
    try:
        fire_insurance_service_fee = int(soup.find_all('span', class_='PriceItem_buttonWrapper__j5wyB')[insurance_or_service_fee].find_next('p').text.replace('R$', '').replace('.', '').strip())
        return fire_insurance_service_fee
    except:
        return 0


def property_features(
        soup: BeautifulSoup, 
        garage: str = None, 
        floors: str = None, 
        bathrooms: str = None, 
        suites: str = None
        ) -> dict:

    """
    Extracts and processes property features from HTML parsed with BeautifulSoup.

    This function scans the feature blocks of a property listing and extracts information such as
    subway proximity, garage spaces, furniture status, floor level, number of bathrooms,
    construction year, number of suites, and whether pets are allowed.

    Parameters:
        soup (BeautifulSoup): The BeautifulSoup object containing the property HTML.
        garage (str, optional): Minimum required number of garage spaces. Values below this threshold are ignored.
        floors (str, optional): Minimum required floor level. Lower floors are ignored.
        bathrooms (str, optional): Minimum required number of bathrooms. Values below this threshold are ignored.
        suites (str, optional): Minimum required number of suites. Values below this threshold are ignored.
    """

    subway = furniture = floor = bathroom = construction_year = pets_field = ''
    qty_suites = qty_garage = 0
    
    divs_features = soup.find_all('div', class_='MuiBox-root mui-15au7ed')

    for div in divs_features[:8]:
        if 'metrô' in div.text or 'próx' in div.text.lower():
            subway = 'Não' if 'sem' in div.text or 'Sem' in div.text or 'Não' in div.text else 'Sim' if 'Próx' in div.text or 'Metrô próx.' in div.text else ''

        if 'vaga' in div.text or 'vagas' in div.text:
            qty_garage = div.text.replace('vagas','').replace('vaga', '').strip()
            if qty_garage.isdigit():
                qty_garage = int(qty_garage)

                if garage and qty_garage < int(garage):
                    qty_garage = 'ignore'
            else:
                qty_garage = 'ignore'

        if 'mobília' in div.text or 'Mobiliado' in div.text:
            furniture = 'Sim' if div.text == 'Mobiliado' else 'Não'

        if 'andar' in div.text:
            floor = div.text
            floor_list = floor.replace('°', '').replace(' andar','')
            floor_list = floor_list.split(' a ') if 'Até' not in floor else floor_list.replace('Até ', '').strip()

            if floors:
                if len(floor_list) == 1:
                    floor = 'ignore' if not int(floors) <= int(floor_list[0]) else floor
                else:
                     floor = floor if int(floors) <= int(floor_list[0]) else floor if int(floors) <= int(floor_list[1]) else 'ignore'

        if 'banheiro' in div.text or 'banheiros' in div.text:
            bathroom = div.text.replace('banheiros', '').replace('banheiro', '').strip()

            if bathroom.isdigit():
                bathroom = int(bathroom)

                if bathrooms and bathroom < int(bathrooms):
                    bathroom = 'ignore'
            else:
                bathroom = 'ignore'

        if '(Construção)' in div.text:
            construction_year = div.find('p').text

        if 'suíte' in div.text or 'suítes' in div.text:
            qty_suites = int(div.text.replace('(','').replace(')', '').replace(' suíte', '').replace(' suítes', '').replace('quarto', '').replace('quartos', '').replace('s', '').split()[-1])
            if suites and qty_suites < int(suites):
                qty_suites = 'ignore'

        if 'aceita' in div.text.lower():
            pets_field = 'Não' if 'Não' in div.text else 'Sim'

    return {
        'subway': subway,
        'garage': qty_garage,
        'furniture': furniture,
        'floor': floor,
        'bathrooms': bathroom,
        'suites': qty_suites,
        'construction_year': construction_year,
        'pets': pets_field
    }

def get_amenities_list(
        soup: BeautifulSoup
        ) -> str:
    
    """
    Extracts all listed amenities from a property page.
    
    Parameters:
        soup (BeautifulSoup): Parsed HTML content of the property page
    """
    try:
        amenities_list = soup.find('div', attrs={
        'data-testid':'amenities-list'
        }).find('div').find('div').find_all('p')
        all_amenities = ', '.join(amenities.text.strip() for amenities in amenities_list)
    except:
        all_amenities = ''
    
    return all_amenities

def get_all_condominium_features(
    soup: BeautifulSoup
    ) -> str:
    
    """
    Retrieves all condominium-level features from the property page.
    
    Parameters:
        soup (BeautifulSoup): Parsed HTML content of the property page.
    """
    
    condominium_features = ''
    condominium_features = soup.find('div', class_='SectionAccordion_descriptionBox__n3wvy').text.strip()
    return condominium_features

def get_publication_date(
    soup: BeautifulSoup
    ) -> str:
    
    """
    Extracts the publication date of the property listing.

    Parameters:
        soup (BeautifulSoup): Parsed HTML content of the property page.
    """

    publication_date = soup.find('small', attrs={
        "data-testid": "publication_date"
    }).text.replace('Publicado ', '')
    return publication_date