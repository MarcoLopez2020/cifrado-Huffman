import json
import huffman
import base64
import heapq
from graphviz import Digraph

# ----------- CIFRADO HUFFMAN ----------------

def cifrar_con_huffman(data):
    simbolos = {}
    for item in data:
        simbolos.update({char: simbolos.get(char, 0) + 1 for char in item["NOMBRES"]})
        simbolos.update({char: simbolos.get(char, 0) + 1 for char in item["APELLIDOS"]})
        simbolos.update({char: simbolos.get(char, 0) + 1 for char in item["email"]})

    if not simbolos:
        return []

    # Crear el código Huffman
    codigo_huffman = huffman.codebook(list(simbolos.items()))

    # Cifrar los datos
    datos_cifrados = []
    for item in data:
        nombres_cifrado = "".join(codigo_huffman[char] for char in item["NOMBRES"])
        apellidos_cifrado = "".join(codigo_huffman[char] for char in item["APELLIDOS"])
        email_cifrado = "".join(codigo_huffman[char] for char in item["email"])
        datos_cifrados.append({
            "NOMBRES_CIFRADO": nombres_cifrado,
            "APELLIDOS_CIFRADO": apellidos_cifrado,
            "email_CIFRADO": email_cifrado
        })

    # Codificar árbol en base64 para guardar
    arbol_codificado = base64.b64encode(json.dumps(dict(codigo_huffman)).encode()).decode()

    # Dibujar y guardar el árbol como imagen
    arbol_raiz = construir_arbol_huffman(simbolos)
    grafico = dibujar_arbol(arbol_raiz)
    grafico.render("arbol_huffman", format="png", cleanup=True)
    print("🌳 Árbol de Huffman guardado como 'arbol_huffman.png'")

    return {
        "datos_cifrados": datos_cifrados,
        "arbol_huffman_codificado": arbol_codificado
    }

def guardar_datos_cifrados(datos_cifrados, nombre_archivo="datos_cifrados.json"):
    with open(nombre_archivo, 'w') as archivo:
        json.dump(datos_cifrados, archivo, indent=2)

# ----------- DECIFRADO HUFFMAN ----------------

def decifrar_con_huffman(datos_cifrados_con_arbol):
    arbol_codificado = datos_cifrados_con_arbol["arbol_huffman_codificado"]
    codigo_huffman_dict = json.loads(base64.b64decode(arbol_codificado).decode())

    decodificador_huffman = {v: k for k, v in codigo_huffman_dict.items()}

    datos_decifrados = []
    for item_cifrado in datos_cifrados_con_arbol["datos_cifrados"]:
        def decodificar_texto(texto_codificado):
            texto_decodificado = ""
            codigo_actual = ""
            for bit in texto_codificado:
                codigo_actual += bit
                if codigo_actual in decodificador_huffman:
                    texto_decodificado += decodificador_huffman[codigo_actual]
                    codigo_actual = ""
            return texto_decodificado

        datos_decifrados.append({
            "NOMBRES": decodificar_texto(item_cifrado["NOMBRES_CIFRADO"]),
            "APELLIDOS": decodificar_texto(item_cifrado["APELLIDOS_CIFRADO"]),
            "email": decodificar_texto(item_cifrado["email_CIFRADO"])
        })

    return datos_decifrados

def cargar_datos_cifrados(nombre_archivo="datos_cifrados.json"):
    with open(nombre_archivo, 'r') as archivo:
        return json.load(archivo)

def guardar_datos_decifrados(datos_decifrados, nombre_archivo="datos_decifrados.json"):
    with open(nombre_archivo, 'w') as archivo:
        json.dump(datos_decifrados, archivo, indent=2)

# ----------- VISUALIZACIÓN DEL ÁRBOL ----------------

class NodoHuffman:
    def __init__(self, simbolo=None, frecuencia=0, izquierda=None, derecha=None):
        self.simbolo = simbolo
        self.frecuencia = frecuencia
        self.izquierda = izquierda
        self.derecha = derecha

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def construir_arbol_huffman(frecuencias):
    heap = [NodoHuffman(simbolo=s, frecuencia=f) for s, f in frecuencias.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        nodo_izq = heapq.heappop(heap)
        nodo_der = heapq.heappop(heap)
        nuevo_nodo = NodoHuffman(
            simbolo=None,
            frecuencia=nodo_izq.frecuencia + nodo_der.frecuencia,
            izquierda=nodo_izq,
            derecha=nodo_der
        )
        heapq.heappush(heap, nuevo_nodo)

    return heap[0] if heap else None

def dibujar_arbol(nodo, dot=None, prefix=""):
    if dot is None:
        dot = Digraph()

    if nodo.simbolo is not None:
        etiqueta = f"{nodo.simbolo} ({nodo.frecuencia})"
        dot.node(prefix, etiqueta)
    else:
        etiqueta = f"{nodo.frecuencia}"
        dot.node(prefix, etiqueta)

        if nodo.izquierda:
            dot.edge(prefix, prefix + "0", label="0")
            dibujar_arbol(nodo.izquierda, dot, prefix + "0")

        if nodo.derecha:
            dot.edge(prefix, prefix + "1", label="1")
            dibujar_arbol(nodo.derecha, dot, prefix + "1")

    return dot

# ----------- EJECUCIÓN PRINCIPAL ----------------

if __name__ == "__main__":
    # Leer datos de entrada desde JSON
    nombre_archivo_entrada = "datos.json"
    with open(nombre_archivo_entrada, 'r') as f:
        datos_originales = json.load(f)

    # Cifrar y guardar
    resultado_cifrado = cifrar_con_huffman(datos_originales)
    guardar_datos_cifrados(resultado_cifrado)
    print("✅ Datos cifrados guardados en datos_cifrados.json")

    # Cargar y decifrar
    datos_cifrados_con_arbol = cargar_datos_cifrados()
    datos_decifrados = decifrar_con_huffman(datos_cifrados_con_arbol)
    guardar_datos_decifrados(datos_decifrados)
    print("✅ Datos decifrados guardados en datos_decifrados.json")
