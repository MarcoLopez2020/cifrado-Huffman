import json
import huffman
import base64

def cifrar_con_huffman(data):
    """Cifra los datos y guarda los datos cifrados junto con el árbol de Huffman."""
    simbolos = {}
    for item in data:
        simbolos.update({char: simbolos.get(char, 0) + 1 for char in item["NOMBRES"]})
        simbolos.update({char: simbolos.get(char, 0) + 1 for char in item["APELLIDOS"]})
        simbolos.update({char: simbolos.get(char, 0) + 1 for char in item["email"]})

    if not simbolos:
        return []

    # ✅ Corrección: convertir a lista de tuplas (símbolo, frecuencia)
    codigo_huffman = huffman.codebook(list(simbolos.items()))

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

    arbol_codificado = base64.b64encode(json.dumps(dict(codigo_huffman)).encode()).decode()

    return {
        "datos_cifrados": datos_cifrados,
        "arbol_huffman_codificado": arbol_codificado
    }

def guardar_datos_cifrados(datos_cifrados, nombre_archivo="datos_cifrados.json"):
    """Guarda los datos cifrados y el árbol en un archivo JSON."""
    with open(nombre_archivo, 'w') as archivo:
        json.dump(datos_cifrados, archivo, indent=2)

def decifrar_con_huffman(datos_cifrados_con_arbol):
    """Decifra los datos utilizando el codebook guardado."""
    arbol_codificado = datos_cifrados_con_arbol["arbol_huffman_codificado"]
    codigo_huffman_dict = json.loads(base64.b64decode(arbol_codificado).decode())

    # Invertir el diccionario para decodificar: código -> carácter
    decodificador_huffman = {v: k for k, v in codigo_huffman_dict.items()}

    datos_decifrados = []
    for item_cifrado in datos_cifrados_con_arbol["datos_cifrados"]:
        nombres_cifrado = item_cifrado["NOMBRES_CIFRADO"]
        apellidos_cifrado = item_cifrado["APELLIDOS_CIFRADO"]
        email_cifrado = item_cifrado["email_CIFRADO"]

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
            "NOMBRES": decodificar_texto(nombres_cifrado),
            "APELLIDOS": decodificar_texto(apellidos_cifrado),
            "email": decodificar_texto(email_cifrado)
        })

    return datos_decifrados

def cargar_datos_cifrados(nombre_archivo="datos_cifrados.json"):
    """Carga los datos cifrados y el árbol desde el archivo JSON."""
    with open(nombre_archivo, 'r') as archivo:
        return json.load(archivo)

def guardar_datos_decifrados(datos_decifrados, nombre_archivo="datos_decifrados.json"):
    """Guarda los datos decifrados en un archivo JSON."""
    with open(nombre_archivo, 'w') as archivo:
        json.dump(datos_decifrados, archivo, indent=2)

# --- Uso de ejemplo ---

# Cifrado
nombre_archivo_entrada = "datos.json"  # Asegúrate de tener este archivo con los datos de entrada
with open(nombre_archivo_entrada, 'r') as f:
    datos_originales = json.load(f)

resultado_cifrado = cifrar_con_huffman(datos_originales)
guardar_datos_cifrados(resultado_cifrado)
print("✅ Datos cifrados y árbol guardados en datos_cifrados.json")

# Decifrado
datos_cifrados_con_arbol = cargar_datos_cifrados()
datos_decifrados = decifrar_con_huffman(datos_cifrados_con_arbol)
guardar_datos_decifrados(datos_decifrados)
print("✅ Datos decifrados y guardados en datos_decifrados.json")
