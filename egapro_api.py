"""
This module is a flask app that serves the EgaPro data, via a JSON API.
It read the data from a CSV file, and serves it as a JSON object.
"""

from csv import DictReader

from flask import Flask, jsonify

# Read the index-egalite-fh.csv file and store it in a dictionary

egapro_data = {}

with open("index-egalite-fh-utf8.csv") as csv:
    reader = DictReader(csv, delimiter=";", quotechar='"')
    for row in reader:
        if egapro_data.get(row["SIREN"]) is None:
            egapro_data[row["SIREN"]] = row
        elif egapro_data[row["SIREN"]]["Année"] < row["Année"]:
            egapro_data[row["SIREN"]].update(row)

application = Flask(__name__)


# Define the SIREN route taking a SIREN as a parameter and returning the
# corresponding data from the egapro_data dictionary
@application.route("/siren/<siren>")
def siren(siren: int):
    """
    Return the EgaPro data for a given SIREN number.
    A 404 is return if the SIREN is not found.

       :param siren: SIREN number as integer
       :return: The corresponding data as a JSON
    """
    response = egapro_data.get(siren)

    if response is None:
        response = {"error": "SIREN not found"}
        status = 404
    else:
        status = 200
    return jsonify(response), status


# A debug flask launcher
if __name__ == "__main__":
    application.run(debug=True)
