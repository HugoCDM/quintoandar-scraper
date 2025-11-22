LOCATION_ABBREVIATIONS = {
        ('rio de janeiro', 'rj'): '-rio-de-janeiro-rj',
        ('sao paulo', 'sp'): '-sao-paulo-sp',
        ('minas gerais', 'mg'): '-minas-gerais-mg',
        ('parana', 'pr'): '-parana-pr',
        ('rio grande do sul', 'rs'): '-rio-grande-do-sul-rs',
        ('santa catarina', 'sc'): '-santa-catarina-sc',
        ('bahia', 'ba'): '-bahia-ba',
        ('distrito federal', 'df'): '-brasilia-df',
        ('goias', 'go'): '-goias-go'
    }

BUY_COLUMNS = ['Anúncio', 'Data de publicação (aproximada)', 'Tipo de imóvel', 'Rua', 'Bairro',
                'Cidade', 'Valor imóvel', 'Área (m²)', 'Quartos', 'Suítes', 'Banheiros',
                'Vagas garagem', 'Condomínio', 'Iptu Mensal (Estimado)', 'Iptu Anual (Estimado)', 'Custo total mensal', 'Próximo ao metrô',
                'Faixa andares', 'Mobília', 'Ano de construção', 'Comodidades',
                'Características condomínio', 'Link']

RENT_COLUMNS = ['Anúncio', 'Data de publicação (aproximada)', 'Tipo de imóvel', 'Rua', 'Bairro',
                'Cidade', 'Valor aluguel', 'Área (m²)', 'Quartos', 'Suítes', 'Banheiros',
                'Vagas garagem', 'Condomínio', 'Iptu Mensal (Estimado)', 'Iptu Anual (Estimado)', 
                'Seguro incêndio', 'Taxa de serviço', 'Custo total mensal', 'Pets', 'Próximo ao metrô',
                'Faixa andares', 'Mobília', 'Ano de construção', 'Comodidades',
                'Características condomínio', 'Link']




PROPERTY_TYPE = {
    '1': 'Apartamento',
    '2': 'Casa',
    '3': 'Casa de condomínio',
    '4': 'Kitnet/Studio',
    '5': 'Todos'
}

FORMATTED_PROPERTY_TYPE = {
    'casa de condomínio': 'Casa de condomínio',
    'apartamento': 'Apartamento',
    'kitnet': 'Kitnet/Studio',
    'studio': 'Kitnet/Studio',
    'casa': 'Casa'
}

CONDOMINIUM_FEATURES = {
    '1': 'academia',
    '2': 'brinquedoteca',
    '3': 'área verde',
    '4': 'churrasqueira',
    '5': 'lavanderia',
    '6': 'elevador',
    '7': 'piscina',
    '8': 'playground',
    '9': 'portaria 24h',
    '10': 'quadra esportiva',
    '11': 'salão de festas',
    '12': 'salão de jogos',
    '13': 'sauna',
    '14': 'todos'
}

AMENITIES_FEATURES = {
    '1': 'apartamento cobertura',
    '2': 'ar condicionado',
    '3': 'banheira',
    '4': 'box',
    '5': 'churrasqueira',
    '6': 'chuveiro a gás',
    '7': 'closet',
    '8': 'garden/área privativa',
    '9': 'novos ou reformados',
    '10': 'piscina privativa',
    '11': 'somente uma casa no terreno',
    '12': 'tanque',
    '13': 'televisão',
    '14': 'utensílios de cozinha',
    '15': 'ventilador de teto',
    '16': 'todos'
}

WELLNESS_FEATURES = {
    '1': 'janelas grandes',
    '2': 'rua silenciosa',
    '3': 'sol da tarde',
    '4': 'sol da manhã',
    '5': 'vista livre',
    '6': 'todos'
}

FURNITURE_FEATURES = {
    '1': 'armários na cozinha',
    '2': 'armários no quarto',
    '3': 'armários nos banheiros',
    '4': 'cama de casal',
    '5': 'cama de solteiro',
    '6': 'mesas e cadeiras de jantar',
    '7': 'sofá',
    '8': 'todos'
}

ACCESSIBILITY_FEATURES = {
    '1': 'banheiro adaptado',
    '2': 'corrimão',
    '3': 'piso tátil',
    '4': 'quartos e corredores com portas amplas',
    '5': 'rampas de acesso',
    '6': 'vaga de garagem acessível',
    '7': 'todos'
}

APPLIANCES_FEATURES = {
    '1': 'fogão',
    '2': 'fogão cooktop',
    '3': 'geladeira',
    '4': 'máquina de lavar',
    '5': 'microondas',
    '6': 'todos'
}

ROOMS_FEATURES = {
    '1': 'área de serviço',
    '2': 'cozinha americana',
    '3': 'home-office',
    '4': 'jardim',
    '5': 'quintal',
    '6': 'varanda',
    '7': 'todos'
}