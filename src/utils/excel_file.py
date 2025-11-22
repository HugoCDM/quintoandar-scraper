from src.config.colors import *
import pandas as pd
from typing import Optional

def create_excel(
        property_list: list, 
        columns: list, 
        choice: str, 
        neighborhood: str, 
        property_value: str
        ) -> Optional[pd.DataFrame]:
    """ 
    Creates and formats an Excel file containing real estate listings scraped from QuintoAndar.

    This function receives a list of property data, converts it into a DataFrame, cleans and 
    normalizes columns, builds Excel-friendly hyperlink formulas, converts numeric fields, and 
    exports a fully formatted Excel file using XlsxWriter.

    Parameters:
        property_list (list): Raw list of scraped property attributes.
        columns (list): Column names that map to property_list fields.
        choice (str): Operation type ("alugar" or "comprar").
        neighborhood (str): Target neighborhood used in filtering.
        property_value (str): Maximum property price used in filtering.
    
    """
    
    str_cols = ['Anúncio', 'Data de publicação (aproximada)', 'Tipo de imóvel', 'Rua', 'Bairro', 'Cidade', 'Próximo ao metrô', 'Faixa andares', 'Mobília', 'Comodidades', 'Características condomínio', 'Link']

    int_cols = ['Área (m²)', 'Quartos', 'Suítes', 'Banheiros', 'Vagas garagem', 'Condomínio', 'Ano de construção', 'Iptu Mensal (Estimado)', 'Iptu Anual (Estimado)', 'Custo total mensal']
    int_cols = int_cols + ['Seguro incêndio', 'Taxa de serviço', 'Valor aluguel'] if choice == 'alugar' else int_cols + ['Valor imóvel']

    df = pd.DataFrame(property_list, columns=columns)

    if df.empty:
        print()
        print(f'{AnsiColors.RED_IGNORE_OR_ERROR}Excel não foi criado por estar vazio e não atender aos parâmetros. Tente novamente!{AnsiColors.RESET}')
        return
    
    df = df[~df.isin(['ignore']).any(axis=1)]
    # df['Condomínio'] = df['Condomínio'].str.replace('.', '')
    df['Anúncio'] = df.apply(lambda col: f'=HYPERLINK("{col["Link"].split('?')[0]}","{col["Anúncio"]}")', axis=1)
    

    for col in int_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    dtype_mapping = {col: str for col in str_cols}
    df = df.astype(dtype_mapping)
    df = df.drop(columns='Link')
    


    caminho_arquivo = f'./files/Imóveis para {choice} - {neighborhood} até {property_value}.xlsx'
    with pd.ExcelWriter(caminho_arquivo, engine='xlsxwriter') as writer:
        nome_aba = 'Imóveis'

        df.to_excel(writer, sheet_name=nome_aba, index=False)

        workbook = writer.book
        worksheet = writer.sheets[nome_aba]

        body_format = workbook.add_format({
            'font_size': 12,
            'align': 'left',
            'valign': 'vcenter'
        })

        header_format = workbook.add_format({
            'bold': True,
            'font_size': 14, 
            'bg_color': '#4472c4',
            'font_color': "#ffffff",
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'

        })

        currency_format = workbook.add_format({
            'num_format': 'R$ #,##0.00',
            'font_size': 12,
            'align': 'left',
            'valign': 'vcenter'
            })  
        
        link_format = workbook.add_format({
            'font_color': '#4472c4',
            'bold': True,
            'font_size': 12,
            'align': 'left',
            'valign': 'vcenter',
            'underline': True
        })

        highlighted_prices_format = workbook.add_format({
            'num_format': 'R$ #,##0.00',
            'font_color': '#1F497D',
            'bold': True,
            'font_size': 12,
            'align': 'left',
            'valign': 'vcenter'
        })

        # header line
        worksheet.set_row(0, 30)

        # columns automatic adjust
        for i, col in enumerate(df.columns):

            
            data_size = df[col].astype(str).map(len).max()
            header_size = len(str(col))
            max_len = max(data_size, header_size) + 10

            worksheet.set_column(i, i, max_len, body_format)
            worksheet.write(0, i, col, header_format)
            
            if pd.isna(data_size):
                data_size = 0
            

            if max_len > 60:
                max_len = 60

            int_cols_transform = ['Valor imóvel', 'Condomínio', 'Iptu Mensal (Estimado)', 'Iptu Anual (Estimado)', 'Custo total mensal'] 
            if choice == 'alugar':
                int_cols_transform += ['Seguro incêndio', 'Taxa de serviço', 'Valor aluguel']

            if col in int_cols_transform: 
                worksheet.set_column(i, i, max_len, currency_format)

            if col in ['Anúncio']:
                worksheet.set_column(i, i, max_len, link_format)

            if col in ['Valor aluguel', 'Valor imóvel', 'Custo total mensal']:
                worksheet.set_column(i, i, max_len, highlighted_prices_format)
                

    print(f'{AnsiColors.GREEN_FILE_SAVED}Arquivo salvo como: Imóveis para {choice} - {neighborhood} até {property_value}.xlsx{AnsiColors.RESET}')
    return df