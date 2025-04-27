import re
import json
from unidecode import unidecode
from fuzzywuzzy import fuzz

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
    :param diccionario_sinonimos: Diccionario que contiene palabras clave y sus sinónimos
    :return: lista de filas con palabras similares
    """
    palabra_limpia = unidecode(palabra.strip().lower())

    filas_similares = []

    for clave, sinomimos in diccionario_sinonimos.items():
        # Comparar palabra ingresada con todos los sinónimos de la clave
        for sinonimo in sinomimos:
            similitud_sinonimo = fuzz.ratio(palabra_limpia, sinonimo)
            if similitud_sinonimo > 80:  # Umbral de similitud
                filas_similares.append({'clave': clave, 'sinonimos': sinomimos})
        
        # Comparar palabra ingresada con la clave
        similitud_clave = fuzz.ratio(palabra_limpia, clave)
        if similitud_clave > 80:  # Umbral de similitud
            filas_similares.append({'clave': clave, 'sinonimos': sinomimos})

    return filas_similares


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

    filas_con_similares = []
    for palabra in palabras:
        similares = obtener_similares(palabra, diccionario_sinonimos)
        filas_con_similares.extend(similares)

    # Crear un array con todas las palabras sin mayúsculas ni tildes
    palabras_encontradas = []
    for fila in filas_con_similares:
        clave = unidecode(fila['clave'].lower())
        palabras_encontradas.append(clave)
        for sinonimo in fila['sinonimos']:
            sinonimo = unidecode(sinonimo.lower())
            palabras_encontradas.append(sinonimo)
    
    print(palabras_encontradas)
    
    resultados = []

    for item in dataset:
        titulo = unidecode(item.get('title', '').lower())

        coincidencias = sum(1 for palabra in palabras_encontradas if palabra in titulo)

        if coincidencias > 0:
            item['coincidencias'] = coincidencias
            resultados.append(item)

    resultados.sort(key=lambda x: x['coincidencias'], reverse=True)
    return resultados
