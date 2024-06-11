from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from csv import DictReader
import requests

egapro_data = {}

with open("index-egalite-fh-utf8.csv", encoding='utf-8') as csv_file:
    reader = DictReader(csv_file, delimiter=";", quotechar='"')
    for row in reader:
        if egapro_data.get(row["SIREN"]) is None:
            egapro_data[row["SIREN"]] = row
        elif egapro_data[row["SIREN"]]["Année"] < row["Année"]:
            egapro_data[row["SIREN"]].update(row)

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