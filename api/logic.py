import re
import json
from unidecode import unidecode

def cargar_diccionario_sinonimos(ruta_diccionario):
    """
    Carga el diccionario de sinónimos desde un archivo JSON o de texto.
    :param ruta_diccionario: Ruta del archivo que contiene los sinónimos.
    :return: Diccionario con palabras clave y sus sinónimos, sin tildes
    """
    diccionario = {}
    if ruta_diccionario.endswith('.json'):
        try:
            with open(ruta_diccionario, 'r', encoding='utf-8') as archivo:
                diccionario = json.load(archivo)
        except FileNotFoundError:
            print(f"El archivo {ruta_diccionario} no se encontró.")
    else:
        try:
            with open(ruta_diccionario, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if ':' in linea:
                        clave, sinomimos_str = linea.split(':', 1)
                        # Eliminar tildes al cargar el diccionario
                        clave = unidecode(clave.strip().lower())
                        sinomimos = [unidecode(s.strip().lower()) for s in sinomimos_str.split(',')]
                        diccionario[clave] = sinomimos
        except FileNotFoundError:
            print(f"El archivo {ruta_diccionario} no se encontró.")
    return diccionario


def obtener_similares(palabra, diccionario_sinonimos):
    """
    Obtiene palabras similares a la palabra de entrada utilizando un diccionario de sinónimos.
    :param palabra: palabra clave
    :param diccionario_sinonimos: Diccionario que contiene palabras clave y sinónimos
    :param top_n: número de palabras similares a obtener
    :return: lista de palabras similares
    """
    palabra_limpia = unidecode(palabra.strip().lower())

    palabras_similares = set()

    for clave, sinomimos in diccionario_sinonimos.items():
        if palabra_limpia == clave:
            palabras_similares.update(sinomimos)
        elif palabra_limpia in sinomimos:
            palabras_similares.add(unidecode(clave.strip().lower()))

    palabras_similares.add(palabra_limpia)
    return list(palabras_similares)

def buscar_convocatorias(palabras_clave, dataset, diccionario_sinonimos):
    """
    Busca las convocatorias que contienen palabras clave o sus sinónimos en el título.
    :param palabras_clave: string separado por espacios o comas
    :param dataset: lista de dicts donde buscar
    :param diccionario_sinonimos: Diccionario con palabras clave y sus sinónimos
    :return: lista de dicts que son relevantes
    """
    palabras = re.split(r'[,\s]+', palabras_clave.strip().lower())
    palabras = [unidecode(p).strip() for p in palabras if p]

    palabras_con_similares = []
    for palabra in palabras:
        similares = obtener_similares(palabra, diccionario_sinonimos)
        palabras_con_similares.extend(similares)
    
    print(palabras_con_similares)
    
    resultados = []

    for item in dataset:
        titulo = unidecode(item.get('title', '').lower())

        coincidencias = sum(1 for palabra in palabras_con_similares if palabra in titulo)

        if coincidencias > 0:
            item['coincidencias'] = coincidencias
            resultados.append(item)

    resultados.sort(key=lambda x: x['coincidencias'], reverse=True)
    return resultados