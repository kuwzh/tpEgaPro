import rpyc

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