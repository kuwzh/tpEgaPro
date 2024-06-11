from csv import DictReader
from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

# Lire le fichier CSV et stocker les données dans un dictionnaire
egapro_data = {}

with open("index-egalite-fh-utf8.csv") as csv:
    reader = DictReader(csv, delimiter=";", quotechar='"')
    for row in reader:
        if egapro_data.get(row["SIREN"]) is None:
            egapro_data[row["SIREN"]] = row
        elif egapro_data[row["SIREN"]]["Année"] < row["Année"]:
            egapro_data[row["SIREN"]].update(row)

application = Flask(__name__)

# Définir la route SIREN
@application.route("/siren/<siren>")
def siren(siren: int):
    """
    Retourne les données EgaPro pour un numéro SIREN donné.
    Renvoie une 404 si le SIREN n'est pas trouvé.

    :param siren: Numéro SIREN en tant qu'entier
    :return: Les données correspondantes sous forme de JSON
    """
    response = egapro_data.get(siren)

    if response is None:
        response = {"error": "SIREN not found"}
        status = 404
    else:
        status = 200
    return jsonify(response), status

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