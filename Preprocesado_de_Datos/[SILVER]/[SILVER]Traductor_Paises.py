import pycountry
from iso3166 import countries_by_name
import gettext

def obtener_codigo_iso(nombre_pais,language='es'):
    nombre_pais=nombre_pais.upper()
    if language!='en':
        try:
            # Busca el país por nombre en inglés
            language = gettext.translation('iso3166', pycountry.LOCALES_DIR, languages=[language])
            language.install()
            _ = language.gettext
            for english_country in pycountry.countries:
                nombre_pais = nombre_pais.lower()
                german_country = _(english_country.name).lower()
                if german_country == nombre_pais:
                    return english_country.alpha_2
        except LookupError:
            # Maneja el caso en el que no se encuentra el país
            return None
    else:
        try:
            # Busca el país por nombre en español
            pais = countries_by_name.get(nombre_pais)
            return pais.alpha2
        except AttributeError:
            # Maneja el caso en el que no se encuentra el país
            return None
        
print(obtener_codigo_iso('EspañA'))
print(obtener_codigo_iso('spain','en'))
