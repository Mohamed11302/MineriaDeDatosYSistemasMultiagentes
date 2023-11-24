from googletrans import Translator

def traducir_al_ingles(nombre_pais):
    traducciones = {
        'Belgica': 'Belgium',
        'Alemania': 'Germany',
        'España': 'Spain',
        'Reino Unido': 'UK',
        'Francia': 'France',
        'Italia': 'Italy',
        'Estados Unidos': 'USA',
        'Chequia': 'Czech Republic',
        'Croacia': 'Croatia',
        'Dinamarca': 'Denmark',
        'Eslovaquia': 'Slovakia',
        'Eslovenia': 'Slovenia',
        'Finlandia': 'Finland',
        'Grecia': 'Greece',
        'Hungría': 'Hungary',
        'Irlanda': 'Ireland',
        'Letonia': 'Latvia',
        'Lituania': 'Lithuania',
        'Luxemburgo': 'Luxembourg',
        'Países Bajos': 'Netherlands',
        'Polonia': 'Poland',
        'Rumanía': 'Romania',
        'Suecia': 'Sweden'
    }
    if nombre_pais in traducciones:
        traduccion = traducciones[nombre_pais]
        return traduccion
    else:
        return nombre_pais
