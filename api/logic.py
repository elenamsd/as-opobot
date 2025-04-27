import re

def buscar_convocatorias(palabras_clave, dataset):
    """
    Busca las convocatorias que contienen palabras clave en el título.
    :param palabras_clave: string separado por espacios o comas
    :param dataset: lista de dicts donde buscar
    :return: lista de dicts que son relevantes
    """
    palabras = re.split(r'[,\s]+', palabras_clave.strip().lower())
    palabras = [p for p in palabras if p]

    resultados = []

    for item in dataset:
        titulo = item.get('title', '').lower()
        coincidencias = sum(1 for palabra in palabras if palabra in titulo)

        if coincidencias > 0:
            item['coincidencias'] = coincidencias
            resultados.append(item)

    resultados.sort(key=lambda x: x['coincidencias'], reverse=True)
    return resultados