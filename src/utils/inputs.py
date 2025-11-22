from unidecode import unidecode
from typing import Optional
from src.config.colors import AnsiColors

def required_inputs(
        text: str,
        response_options: Optional[list] = None
        ) -> str:

    """
    Inserts mandatory input values that cannot be skipped.

    Parameters:
        text: message displayed to the user when requesting input.
        response_options: optional list of predefined valid values. Default: None.
    """

    question = f'{AnsiColors.YELLOW_ITALIC_QUESTION}{text.strip()}{AnsiColors.RESET}'
    if response_options:
        response_options = [option.lower() for option in response_options]
        question += ' (' + '/'.join(option for option in response_options) + '): '
    else:
        question += ': '

    while True:
        value = input(question).strip().lower()
        if not value:
            print(f'{AnsiColors.RED_IGNORE_OR_ERROR}Campo obrigatório. Por favor, preencher!{AnsiColors.RESET}')
            continue
        if response_options and value not in response_options:
            print(f'{AnsiColors.RED_IGNORE_OR_ERROR}Opção inválida! Escolhas disponíveis: ({", ".join(response_options)}){AnsiColors.RESET}')
            continue

        return value

def numeric_inputs(
        text: str,
        optional: bool = True
        ) -> str:
    """
    Handles inputs consisting of numeric values.

    Parameters:
        text: message displayed to the user when requesting input.
        optional: enables an 'ignore' option in the prompt. Default: True.
    """


    new_text = f' {AnsiColors.RED_IGNORE_OR_ERROR}(Enter para ignorar){AnsiColors.RESET}: ' if optional else ': '

    while True:
        value = input(f'{AnsiColors.YELLOW_ITALIC_QUESTION}{text.strip()}{AnsiColors.RESET}{new_text}').strip()

        if not value and optional:
            return ''

        if value.isnumeric():
            return value
        print(f'{AnsiColors.RED_IGNORE_OR_ERROR}Por favor, digite um value numérico válido!{AnsiColors.RESET}')


def range_inputs(
        text: str,
        min: int,
        max: int,
        options: Optional[dict] = None,
        optional: bool = True,
        multiple: bool = True
        ) -> str:
    """
    Handles inputs constrained to a specific numeric range [min-max], e.g., range(1, 4).

    Parameters:
        text: message displayed to the user when requesting input.
        min and max: minimum and maximum values allowed in the range.
        options: dictionary containing the options to be displayed on screen.
        optional: enables an 'ignore' option in the prompt. Default: True.
        multiple: allows the user to select multiple values. Default: True.
    """

    text = f'{AnsiColors.YELLOW_ITALIC_QUESTION}{text}{AnsiColors.RESET}'
    options_dict = ''

    if options:
        for key, value in options.items():
            options_dict += f'[{key}] {value}\n'
        text += f'\n{options_dict}'

    else:
        text += f' (Digite entre {min} e {max}) '

    if multiple:
        text += f'{AnsiColors.BLUE_SEPARATE_MULTIPLE_OPTIONS}(Separe múltiplas opções por vírgula, por exemplo: 1, 2, 3 ou Todos para selecionar todas as opções){AnsiColors.RESET} '

    if optional:
        text += f'{AnsiColors.RED_IGNORE_OR_ERROR}(Enter para ignorar){AnsiColors.RESET}: '
    else:
        text += 'Digite: '

    while True:
        value = input(text).strip()

        
        if not value and optional:
            return ''

        
        if multiple:
            values = [v.strip() for v in value.split(',')]

            valid_values = []
            error = False

            for v in values:
                if not v.isdigit():
                    print()
                    print(f'{AnsiColors.RED_IGNORE_OR_ERROR}"{v}" não é um número válido!{AnsiColors.RESET}')
                    error = True
                    break

                if int(v) not in range(int(min), int(max + 1)):
                    print()
                    print(f'{AnsiColors.RED_IGNORE_OR_ERROR}"{v}" está fora do intervalo {min}-{max}!{AnsiColors.RESET}')
                    error = True
                    break

                valid_values.append(v)

            if error:
                continue

            return ', '.join(options[text] for text in valid_values)

        else:
            if not value.isdigit():
                print()
                print(f'{AnsiColors.RED_IGNORE_OR_ERROR}Por favor, digite um número válido!{AnsiColors.RESET}')
                continue

            if int(value) in range(int(min), int(max + 1)):
                return value

            print()
            print(f'{AnsiColors.RED_IGNORE_OR_ERROR}Por favor, digite um value entre {min} e {max}!{AnsiColors.RESET}')


def yes_no_inputs(
        text: str,
        optional: bool = True,
        options: Optional[list] = None
        ) -> str:

    """
    Inputs with selectable [yes/no] choices.

    Parameters:
        text: message displayed to the user when requesting input.
        optional: enables an 'ignore' option in the prompt. Default: True.
        options: list of options to display on screen (e.g., ['Sim', 'Não']). 
    """

    if options is None:
        options = ['Sim', 'Não']

    new_text = ''
    options_list = [unidecode(op.lower()) for op in options]

    if optional:
        new_text += f' ({"/".join(options_list)}) {AnsiColors.RED_IGNORE_OR_ERROR}(Enter para ignorar){AnsiColors.RESET}'
    else:
        new_text += f' ({"/".join(options_list)})'

    while True:
        value = input(f'{AnsiColors.YELLOW_ITALIC_QUESTION}{text}{AnsiColors.RESET}{new_text}: ').strip().lower()
        normalized_value = unidecode(value)

        if not value and optional:
            return ''

        if normalized_value in options_list:
            return value
        print(f'{AnsiColors.RED_IGNORE_OR_ERROR}Por favor, digite ou {options_list[0]} ou {options_list[1]}{AnsiColors.RESET}')

