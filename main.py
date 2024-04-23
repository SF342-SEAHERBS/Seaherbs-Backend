from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD
from rdflib import Variable
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Create a Graph
g = Graph()

# Bind a namespace
onto = Namespace("http://www.w3.org/2002/07/owl#")

# Load the RDF data from the ontology file
g.parse("ontology.rdf")


@app.route("/")
def index():
    return "Server is running"


@app.route("/sparql", methods=["POST"])
def sparql():
    herb_name = request.json["herbName"]
    try:
        query = (
            """
            PREFIX onto: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?name ?otherName ?synonym ?binomialName ?family ?englishName ?pharmacology ?origin ?medicalProperties ?character ?properties
            WHERE {
              ?herb rdf:type onto:FreshHerb .
              ?herb onto:hasName ?name .
              OPTIONAL { ?herb onto:hasOtherName ?otherName }
              OPTIONAL { ?herb onto:hasSynonym ?synonym }
              OPTIONAL { ?herb onto:hasBinomialName ?binomialName }
              OPTIONAL { ?herb onto:hasFamily ?family }
              OPTIONAL { ?herb onto:hasEnglishName ?englishName }
              OPTIONAL { ?herb onto:hasPharmacology ?pharmacology }
              OPTIONAL { ?herb onto:hasOrigin ?origin }
              OPTIONAL { ?herb onto:hasMedicalProperties ?medicalProperties }
              OPTIONAL { ?herb onto:hasCharacter ?character }
              OPTIONAL { ?herb onto:hasProperties ?properties }
              FILTER (?name = "%s")
            }
            LIMIT 1
        """
            % herb_name
        )

        result_herb_info = g.query(query)
        data = []
        for row in result_herb_info:
            data.append(
                {
                    "name": row["name"],
                    "otherName": row["otherName"] if row["otherName"] else None,
                    "synonym": row["synonym"] if row["synonym"] else None,
                    "binomialName": (
                        row["binomialName"] if row["binomialName"] else None
                    ),
                    "family": row["family"] if row["family"] else None,
                    "englishName": row["englishName"] if row["englishName"] else None,
                    "pharmacology": (
                        row["pharmacology"] if row["pharmacology"] else None
                    ),
                    "origin": row["origin"] if row["origin"] else None,
                    "medicalProperties": (
                        row["medicalProperties"] if row["medicalProperties"] else None
                    ),
                    "character": row["character"] if row["character"] else None,
                    "properties": row["properties"] if row["properties"] else None,
                }
            )
        return jsonify(data)
    except Exception as e:
        print("Error executing SPARQL query:", e)
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(port=3001)
