import heapq
import json
from graphviz import Digraph


class NodoHuffman:
    def __init__(self, simbolo=None, frecuencia=0, izquierda=None, derecha=None):
        self.simbolo = simbolo
        self.frecuencia = frecuencia
        self.izquierda = izquierda
        self.derecha = derecha

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia


def contar_frecuencias(data):
    frecuencias = {}
    for item in data:
        for key in ["NOMBRES", "APELLIDOS", "email"]:
            for char in item[key]:
                frecuencias[char] = frecuencias.get(char, 0) + 1
    return frecuencias


def construir_arbol_huffman(frecuencias):
    heap = [NodoHuffman(s, f) for s, f in frecuencias.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        nodo1 = heapq.heappop(heap)
        nodo2 = heapq.heappop(heap)
        combinado = NodoHuffman(None, nodo1.frecuencia + nodo2.frecuencia, nodo1, nodo2)
        heapq.heappush(heap, combinado)

    return heap[0] if heap else None


def generar_codigos(nodo, camino="", codigos=None):
    if codigos is None:
        codigos = {}
    if nodo.simbolo is not None:
        codigos[nodo.simbolo] = camino
    else:
        if nodo.izquierda:
            generar_codigos(nodo.izquierda, camino + "0", codigos)
        if nodo.derecha:
            generar_codigos(nodo.derecha, camino + "1", codigos)
    return codigos


def codificar_datos(data, codigos):
    datos_cifrados = []
    for item in data:
        cifrado = {}
        for key in ["NOMBRES", "APELLIDOS", "email"]:
            cifrado[f"{key}_CIFRADO"] = ''.join(codigos[char] for char in item[key])
        datos_cifrados.append(cifrado)
    return datos_cifrados


def decodificar_texto(cifrado, codigos):
    inverso = {v: k for k, v in codigos.items()}
    actual, resultado = "", ""
    for bit in cifrado:
        actual += bit
        if actual in inverso:
            resultado += inverso[actual]
            actual = ""
    return resultado


def decodificar_datos(datos_cifrados, codigos):
    return [{
        "NOMBRES": decodificar_texto(item["NOMBRES_CIFRADO"], codigos),
        "APELLIDOS": decodificar_texto(item["APELLIDOS_CIFRADO"], codigos),
        "email": decodificar_texto(item["email_CIFRADO"], codigos)
    } for item in datos_cifrados]


def dibujar_arbol(nodo, dot=None, nombre="arbol_huffman"):
    if dot is None:
        dot = Digraph()

    def recorrer(nodo, id):
        etiqueta = f"{nodo.simbolo} ({nodo.frecuencia})" if nodo.simbolo else str(nodo.frecuencia)
        dot.node(id, etiqueta)
        if nodo.izquierda:
            dot.edge(id, id + "0", label="0")
            recorrer(nodo.izquierda, id + "0")
        if nodo.derecha:
            dot.edge(id, id + "1", label="1")
            recorrer(nodo.derecha, id + "1")

    recorrer(nodo, "0")
    dot.render(f"static/{nombre}", format="png", cleanup=True)
