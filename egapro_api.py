from csv import DictReader
from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

egapro_data = {}

# Lecture des données depuis le fichier CSV lors du chargement de l'application
with open("C:/Users/Neil/source/repos/tpEgaPro/index-egalite-fh-utf8.csv", encoding="utf-8") as csv_file:
    reader = DictReader(csv_file, delimiter=";", quotechar='"')
    for row in reader:
        if egapro_data.get(row["SIREN"]) is None:
            egapro_data[row["SIREN"]] = row
        elif egapro_data[row["SIREN"]]["Année"] < row["Année"]:
            egapro_data[row["SIREN"]].update(row)

@app.route("/api/siren/<int:siren>", methods=["GET"])
def get_data_by_siren(siren):
    data = egapro_data.get(str(siren))
    if not data:
        return jsonify({"error": "SIREN not found"}), 404
    return jsonify(data), 200

# Configuration de Swagger UI
SWAGGER_URL = '/api/docs'  # URL pour accéder à la documentation Swagger UI
API_URL = '/swagger.json'   # URL de votre documentation Swagger JSON

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "EgaPro API"
    }
)

# Enregistrer la documentation Swagger UI dans l'application Flask
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Définissez la route pour générer le fichier swagger.json
@app.route('/swagger.json')
def create_swagger_spec():
    # Définissez ici votre spécification Swagger
    swagger_spec = {
        "swagger": "2.0",
        "info": {
            "title": "EgaPro API",
            "description": "API for EgaPro data distribution",
            "version": "1.0"
        },
        # Définissez vos endpoints ici
        "paths": {
            "/api/siren/{siren}": {
                "get": {
                    "description": "Get data by SIREN number",
                    "parameters": [
                        {
                            "name": "siren",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "schema": {
                                # Définissez ici le schéma de votre réponse JSON
                            }
                        },
                        "404": {
                            "description": "SIREN not found"
                        }
                    }
                }
            }
        }
    }
    return jsonify(swagger_spec)

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)
