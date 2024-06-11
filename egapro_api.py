from csv import DictReader
from flask import Flask, jsonify

app = Flask(__name__)

egapro_data = {}

# Lecture des données depuis le fichier CSV lors du chargement de l'application
with open("index-egalite-fh-utf8.csv", encoding="utf-8") as csv_file:
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

if __name__ == "__main__":
    app.run(debug=True)