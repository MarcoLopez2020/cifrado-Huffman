from flask import Flask, render_template, request, redirect, url_for
import json
import os
from huffman_manual import *

app = Flask(__name__)

DATA_FILE = "datos.json"

def leer_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def guardar_datos(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = ""
    datos = leer_datos()

    if request.method == "POST":
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        email = request.form["email"]

        nuevo = {"NOMBRES": nombres, "APELLIDOS": apellidos, "email": email}
        datos.append(nuevo)
        guardar_datos(datos)

        mensaje = "✅ Datos añadidos correctamente."

    if datos:
        frecuencias = contar_frecuencias(datos)
        arbol = construir_arbol_huffman(frecuencias)
        codigos = generar_codigos(arbol)
        cifrado = codificar_datos(datos, codigos)
        decifrado = decodificar_datos(cifrado, codigos)
        dibujar_arbol(arbol)

        return render_template("index.html", datos=datos, codigos=codigos,
                               cifrado=cifrado, decifrado=decifrado,
                               mensaje=mensaje, imagen_arbol="arbol_huffman.png")
    else:
        return render_template("index.html", datos=[], mensaje="No hay datos aún.")

if __name__ == "__main__":
    app.run(debug=True)
