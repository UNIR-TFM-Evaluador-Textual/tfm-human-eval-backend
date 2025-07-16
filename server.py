from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

ANUNCIOS_FILE = "anuncios.json"
CALIFICACIONES_FILE = "calificaciones.json"
CARPETA_IMAGENES = "imagenes"

# Crear archivos si no existen
if not os.path.exists(ANUNCIOS_FILE):
	with open(ANUNCIOS_FILE, "w", encoding="utf-8") as f:
		json.dump([], f, indent=2, ensure_ascii=False)

if not os.path.exists(CALIFICACIONES_FILE):
	with open(CALIFICACIONES_FILE, "w", encoding="utf-8") as f:
		json.dump([], f, indent=2, ensure_ascii=False)

@app.route("/anuncios", methods=["GET"])
def obtener_anuncios():
	with open(ANUNCIOS_FILE, encoding="utf-8") as f:
		anuncios = json.load(f)

	# Parámetros de rango
	inicio = int(request.args.get("inicio", 0))
	fin = request.args.get("fin")

	if fin is not None:
		fin = int(fin)
		anuncios = anuncios[inicio:fin]
	else:
		anuncios = anuncios[inicio:]

	return jsonify(anuncios)

@app.route("/imagenes/<path:nombre_imagen>")
def servir_imagen(nombre_imagen):
	return send_from_directory(CARPETA_IMAGENES, nombre_imagen)

@app.route("/calificar", methods=["POST"])
def guardar_calificacion():
	data = request.json
	if not data or "id" not in data:
		return jsonify({"error": "Faltan datos o ID"}), 400

	# Leer archivo actual
	with open(CALIFICACIONES_FILE, encoding="utf-8") as f:
		calificaciones = json.load(f)

	# Buscar si ya existe una evaluación con ese ID
	actualizado = False
	for i, item in enumerate(calificaciones):
		if item["id"] == data["id"]:
			calificaciones[i] = data
			actualizado = True
			break

	# Si no se encontró, agregar nueva
	if not actualizado:
		calificaciones.append(data)

	# Guardar el archivo
	with open(CALIFICACIONES_FILE, "w", encoding="utf-8") as f:
		json.dump(calificaciones, f, indent=2, ensure_ascii=False)

	return jsonify({
		"mensaje": "Calificación actualizada" if actualizado else "Calificación guardada"
	}), 200



if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
