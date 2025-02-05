
# Lecture des données depuis le fichier CSV lors du chargement de l'application
with open("C:/Users/Neil/source/repos/tpEgaPro/index-egalite-fh-utf8.csv", encoding="utf-8") as csv_file:
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from csv import DictReader
from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

egapro_data = {}
import rpyc
import requests

egapro_data = {}

with open("index-egalite-fh-utf8.csv", encoding='utf-8') as csv_file:
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

class EgaProService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def getEgaProData(ctx, siren):
        """
        Returns the EgaPro data for a given SIREN number.
        """
        data = egapro_data.get(siren)
        if data is None:
            return "SIREN not found"
        return str(data)

# Create a Spyne application
application = Application([EgaProService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

# Create a WSGI application
wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    # Start the WSGI server
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8000, wsgi_application)
    print("Listening on port 8000...")
    server.serve_forever()

    # Example of sending a SOAP request
    soap_request = """<?xml version="1.0" encoding="UTF-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="spyne.examples.hello.soap">
       <soap:Body>
          <ns1:getEgaProData>
             <siren>431796960</siren>
          </ns1:getEgaProData>
       </soap:Body>
    </soap:Envelope>
    """

    # Define the URL of the SOAP service
    url = "http://localhost:8000/"

    # Send the SOAP request
    response = requests.post(url, data=soap_request, headers={"Content-Type": "text/xml"})

    # Print the response content
    print(response.content)

class EgaProService(rpyc.Service):
    def exposed_get_data(self, siren):
        with open("index-egalite-fh-utf8.csv", encoding="utf-8") as csv_file:
            reader = DictReader(csv_file, delimiter=";", quotechar='"')
            for row in reader:
                if row["SIREN"] == siren:
                    return row
        return None

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    server = ThreadedServer(EgaProService, port=18861)
    print("RPC server running on port 18861")
    server.start()
