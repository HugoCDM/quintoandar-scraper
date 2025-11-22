from src.utils.inputs import *
from src.config.constants import *
from src.scraper.quinto_andar import search_listings

def main():
    print('-----------------------------------------------------------------------------------------')
    print('\033[1;32mBuscador de apartamentos para comprar e alugar - Quinto Andar\033[m')
    print('-----------------------------------------------------------------------------------------')

    property_value = rooms = area = furnished = garage = near_subway = suites = cond_iptu = floors = bathrooms = condominium_features = wellness_features = amenities_features = furniture_features = accessibility_features = appliances_features = rooms_features = pets = availability =''

    neighborhood = required_inputs('Digite o bairro / rua desejado')
    city = required_inputs('Digite a cidade / sigla do estado desejado (Exemplo: rio de janeiro ou rj)')
    print()
    property_type = range_inputs('Tipo de imóvel',  1, 5, PROPERTY_TYPE)

    print()
    choice = required_inputs('Comprar ou alugar o imóvel?', ['comprar', 'alugar'])
    property_value = numeric_inputs(f'Qual o valor máximo para {choice} o imóvel', optional=False)
    print('-----------------------------------------------------------------------------------------')

    additional = yes_no_inputs('Vai precisar acrescentar mais informações?', optional=False)

    if additional == 'sim':
        rooms = range_inputs('Quantos quartos?', 1, 4, multiple=False)
        area = numeric_inputs('Quantos m² mínimos o apartamento?', )
        furnished = yes_no_inputs('Vai ser mobiliado?')
        garage = range_inputs('Vai ter espaço na garagem?', 1, 3, multiple=False)
        near_subway = yes_no_inputs('Vai ser próximo ao metrô?')
        suites = range_inputs('Vai possuir quantas suítes?', 1, 4, multiple=False)

        if choice.lower() == 'comprar':
            cond_iptu = numeric_inputs('Valor máximo do iptu + condominio?')

        floors = numeric_inputs('A partir de quantos andares você quer procurar imóveis?')

        bathrooms = range_inputs('Quantos banheiros seriam?', 1, 4, multiple=False)
        print('-----------------------------------------------------------------------------------------')


        if choice.lower() == 'alugar':
            pets = yes_no_inputs('Procura um AP que aceite pets?')
            availability = yes_no_inputs('Disponibilidade do ap?', options=['Imediata', 'Em breve'])

        print('Categorias:')
        print()

        condominium_features = range_inputs('Vai possuir algo da lista?', 1, 14, CONDOMINIUM_FEATURES)
        print()

        amenities_features = range_inputs('Algumas comodidades lhe interessam?', 1, 16, AMENITIES_FEATURES)
        print()

        wellness_features = range_inputs('Alguma(s) característica(s) de bem-estar a seguir é/são interessante(s)?', 1, 6, WELLNESS_FEATURES)
        print()

        furniture_features = range_inputs('Quais mobílias lhe interessam?', 1, 8, FURNITURE_FEATURES)
        print() 

        accessibility_features = range_inputs('Precisa de itens para acessibilidade?', 1, 7, ACCESSIBILITY_FEATURES)
        print()

        appliances_features = range_inputs('Vai precisar de eletrodomésticos disponíveis?', 1, 6, APPLIANCES_FEATURES)
        print()
        rooms_features = range_inputs('Vai precisar de comodos específicos?', 1, 7, ROOMS_FEATURES)


    
    search_listings(additional, neighborhood, city, property_type, property_value, choice, rooms, area, garage, furnished, near_subway, suites, cond_iptu, floors, bathrooms, condominium_features, wellness_features, amenities_features, furniture_features, accessibility_features, appliances_features, rooms_features, pets, availability)
    print()


if __name__ == '__main__':
    main()