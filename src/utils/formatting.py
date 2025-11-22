from unidecode import unidecode
from src.config.constants import *

def build_link(
        neighborhood: str,
        city: str,
        choice: str
        ) -> str:

    """
    Build a QuintoAndar search URL using the provided parameters.

    Parameters:
        neighborhood: neighborhood or street to be included in the search query.
        city: city name or state abbreviation (e.g., 'rj', 'sp').
        choice: type of search, either 'comprar' (buying) or 'alugar' (renting).
    """

    

    normalized_neighborhood = unidecode(neighborhood.lower().replace(' ', '-'))
    city = unidecode(city.lower())
    for key, value in LOCATION_ABBREVIATIONS.items():
        for item in key:
            if item in city:
                city = value
    if normalized_neighborhood.endswith('-'):
        separator = ''
    else:
        separator = '-'

    link = f"https://www.quintoandar.com.br/{choice}/imovel/{normalized_neighborhood}{city}-brasil/"
    print('Link:', link)
    return link


def unidecode_features(
        text: str,
        split: bool = True
        ) -> str:

    """
    Normalize text by converting it to lowercase, removing accents, and optionally splitting it into a list.

    Parameters:
        text: the text to be normalized.
        split: whether to split the text using ', ' before normalization. Default: True.
    """

    text = unidecode(text.lower().strip())
    text = text.split(', ') if split else text
    
    return text

