import rpyc
from csv import DictReader
 
egapro_data = {}
 
with open("index-egalite-fh-utf8.csv") as csv:
    reader = DictReader(csv, delimiter=";", quotechar='"')
    for row in reader:
        if egapro_data.get(row["SIREN"]) is None:
            egapro_data[row["SIREN"]] = row
        elif egapro_data[row["SIREN"]]["Année"] < row["Année"]:
            egapro_data[row["SIREN"]].update(row)
 
class EgaProService(rpyc.Service):
    def on_connect(self, conn):
        pass
 
    def on_disconnect(self, conn):
        pass
 
    def exposed_get_data(self, siren):
        """
        Retourne les données EgaPro pour un numéro SIREN donné.
        """
        return egapro_data.get(str(siren), "SIREN not found")
 
if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(EgaProService, port=18861)
    t.start()