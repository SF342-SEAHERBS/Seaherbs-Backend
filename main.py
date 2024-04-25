from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD
from rdflib import Variable
from rdflib.term import URIRef
from flask import Flask, request, jsonify, Response
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)




# Create a Graph
g = Graph()

# Bind a namespace
onto = Namespace("http://www.w3.org/2002/07/owl#")

# Load the RDF data from the ontology file
g.parse("SEAHERS_Ontology.rdf")


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
              OPTIONAL { ?herb onto:hasBinomailName ?binomialName }
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


# Solution 1: Use POST in the http method to get all the data from the ontology.rdf file.
# But this type of output will be displayed in JSON Object. (Umm.. I think this type of response is JSON.)
# I suggest this is the best function for getAllData. 
# Because when you use the front end, You can convert it to JSON very easily.
@app.route("/post/getAllData", methods=["POST"])
def getAllDataFromPostMethod():
    try:
        query = """
            PREFIX onto: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?subject ?predicate ?object
            WHERE {
              ?subject ?predicate ?object .
            }
            LIMIT 100
        """
        result_herb_info = g.query(query)
        data = []
        for row in result_herb_info:
            data.append(
                {
                    "subject": row["subject"],
                    "predicate": row["predicate"],
                    "object": row["object"],
                }
            )
        data_response = jsonify(data)
        return data_response
    except Exception as e:
        print("Error executing SPARQL query:", e)
        return jsonify({"error": "Internal Server Error"}), 500
    
# Solution 2: Use GET in the http method to get all the data from the ontology.rdf file.
# But this type of output will be displayed in message text or a string.  (Umm.. I think this type of response is message text.)
@app.route("/get/getAllData", methods=["GET"])
def getAllDataFromGetMethod():
    try:
        query = """
            PREFIX onto: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?subject ?predicate ?object
            WHERE {
              ?subject ?predicate ?object .
            }
            LIMIT 100
        """
        result_herb_info = g.query(query)
        data = []
        for row in result_herb_info:
            data.append(
                {
                    "subject": row["subject"],
                    "predicate": row["predicate"],
                    "object": row["object"],
                }
            )
        data_response = json.dumps(data, ensure_ascii=False)
        return data_response
    except Exception as e:
        print("Error executing SPARQL query:", e)
        return jsonify({"error": "Internal Server Error"}), 500
    
    
#3
@app.route("/post2/getAllData", methods=["POST"])
def getAllDataFromPost2Method():
    try:
        query = """
        PREFIX onto: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?name ?otherName ?synonym ?binomialName ?family ?englishName ?pharmacology ?origin ?character ?properties ?urlpicture ?genusName ?specificName ?ecology ?chemical ?toxicology ?howToUse ?reference
        WHERE {
          ?herb onto:hasName ?name .
          OPTIONAL { ?herb onto:hasOtherName ?otherName }
          OPTIONAL { ?herb onto:hasSynonym ?synonym }
          OPTIONAL { ?herb onto:hasBinomailName ?binomialName }
          OPTIONAL { ?herb onto:hasFamily ?family }
          OPTIONAL { ?herb onto:hasEnglishName ?englishName }
          OPTIONAL { ?herb onto:hasPharmacology ?pharmacology }
          OPTIONAL { ?herb onto:Origin ?origin }
          OPTIONAL { ?herb onto:hasCharacter ?character }
          OPTIONAL { ?herb onto:hasProperties ?properties }
          OPTIONAL { ?herb onto:UrlPicture ?urlpicture }
          OPTIONAL { ?herb onto:hasGenusName ?genusName }
          OPTIONAL { ?herb onto:hasSpecificName ?specificName }
          OPTIONAL { ?herb onto:hasEcology ?ecology }
          OPTIONAL { ?herb onto:hasChemical ?chemical }
          OPTIONAL { ?herb onto:hasToxicology ?toxicology }
          OPTIONAL { ?herb onto:hasHowToUse ?howToUse }
          OPTIONAL { ?herb onto:Reference ?reference }
        }
        LIMIT 1000
        """
            
        result_herb_info = g.query(query)
        data = []
        for row in result_herb_info:
            herbName = [herb["name"] for herb in data]
            if str(row["name"]) not in herbName:
                synonymQuery = (
                    """
                    PREFIX onto: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

                    SELECT ?synonym ?name
                    WHERE {
                        
                        ?herb onto:hasName ?name .
                        ?herb onto:hasSynonym ?synonym .
                        OPTIONAL { ?herb onto:hasSynonym ?synonym }
                        FILTER (?name = "%s")
                    }
                    """
                    % str(row["name"])
                )
                result_synonym = g.query(synonymQuery)
                synonymList = [syn["synonym"] for syn in result_synonym]
                
                otherNameQuery = (
                    """
                    PREFIX onto: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

                    SELECT ?otherName ?name
                    WHERE {
                        ?herb onto:hasName ?name .
                        ?herb onto:hasOtherName ?otherName .
                        OPTIONAL { ?herb onto:hasOtherName ?otherName }
                        FILTER (?name = "%s")
                    }
                    """
                    % str(row["name"])
                )
                result_other_name = g.query(otherNameQuery)
                otherNameList = [oth["otherName"] for oth in result_other_name]

                data.append(
                    {
                        "name": str(row["name"]),
                        "otherName":otherNameList,
                        "synonyms": synonymList,
                        "binomialName": (
                            row["binomialName"] if row["binomialName"] else None
                        ),
                        "family": row["family"] if row["family"] else None,
                        "englishName": (
                            row["englishName"] if row["englishName"] else None
                        ),
                        "pharmacology": (
                            row["pharmacology"] if row["pharmacology"] else None
                        ),
                        "origin": row["origin"] if row["origin"] else None,
                        
                        "properties": row["properties"] if row["properties"] else None,
                        "urlpicture": row["urlpicture"] if row["urlpicture"] else None,
                        "genusName": row["genusName"] if row["genusName"] else None,
                        "specificName": row["specificName"] if row["specificName"] else None,
                        "ecology": row["ecology"] if row["ecology"] else None,
                        "chemical": row["chemical"] if row["chemical"] else None,
                        "toxicology": row["toxicology"] if row["toxicology"] else None,
                        "howToUse": row["howToUse"] if row["howToUse"] else None,
                        "reference": row["reference"] if row["reference"] else None,
                        "character": row["character"] if row["character"] else None
                    }
                )

        return jsonify(data)
    except Exception as e:
        print("Error executing SPARQL query:", e)
        return jsonify({"error": "Internal Server Error"}), 500



if __name__ == "__main__":
    app.run(port=3001)
