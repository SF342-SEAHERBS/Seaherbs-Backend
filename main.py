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


# 3
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
        LIMIT 5000
        """

        result_herb_info = g.query(query)
        data = []
        for row in result_herb_info:
            herbName = [herb["name"] for herb in data]
            if str(row["name"]) not in herbName:
                synonymQuery = """
                    PREFIX onto: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

                    SELECT ?synonym ?name
                    WHERE {
                        
                        ?herb onto:hasName ?name .
                        ?herb onto:hasSynonym ?synonym .
                        OPTIONAL { ?herb onto:hasSynonym ?synonym }
                        FILTER (?name = "%s")
                    }
                    """ % str(
                    row["name"]
                )
                result_synonym = g.query(synonymQuery)
                synonymList = [syn["synonym"] for syn in result_synonym]

                otherNameQuery = """
                    PREFIX onto: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

                    SELECT ?otherName ?name
                    WHERE {
                        ?herb onto:hasName ?name .
                        ?herb onto:hasOtherName ?otherName .
                        OPTIONAL { ?herb onto:hasOtherName ?otherName }
                        FILTER (?name = "%s")
                    }
                    """ % str(
                    row["name"]
                )
                result_other_name = g.query(otherNameQuery)
                otherNameList = [oth["otherName"] for oth in result_other_name]

                data.append(
                    {
                        "name": str(row["name"]),
                        "otherName": otherNameList,
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
                        "specificName": (
                            row["specificName"] if row["specificName"] else None
                        ),
                        "ecology": row["ecology"] if row["ecology"] else None,
                        "chemical": row["chemical"] if row["chemical"] else None,
                        "toxicology": row["toxicology"] if row["toxicology"] else None,
                        "howToUse": row["howToUse"] if row["howToUse"] else None,
                        "reference": row["reference"] if row["reference"] else None,
                        "character": row["character"] if row["character"] else None,
                    }
                )

        return jsonify(data)
    except Exception as e:
        print("Error executing SPARQL query:", e)
        return jsonify({"error": "Internal Server Error"}), 500


from rdflib.plugins.sparql import prepareQuery
from flask import jsonify


@app.route("/origin", methods=["POST"])
def origin():
    origin_name = request.json["name"]
    try:
        # Prepare SPARQL query
        query = prepareQuery(
            f"""
            SELECT ?name ?otherName ?synonym ?binomialName ?family ?englishName ?pharmacology ?origin ?character ?properties ?urlpicture ?genusName ?specificName ?ecology ?chemical ?toxicology ?howToUse ?reference
            WHERE {{
                ?herb <http://www.w3.org/2002/07/owl#isInOrigin> <http://www.w3.org/2002/07/owl#{origin_name}> .
                ?herb <http://www.w3.org/2002/07/owl#hasName> ?name .
                ?herb <http://www.w3.org/2002/07/owl#UrlPicture> ?urlpicture .
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasOtherName> ?otherName . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasSynonym> ?synonym . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasBinomialName> ?binomialName . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasFamily> ?family . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasEnglishName> ?englishName . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasPharmacology> ?pharmacology . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#Origin> ?origin . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasCharacter> ?character . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasProperties> ?properties . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasGenusName> ?genusName . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasSpecificName> ?specificName . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasEcology> ?ecology . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasToxicology> ?toxicology . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasChemical> ?chemical . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasHowToUse> ?howToUse . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#Reference> ?reference . }}
            }}
        """,
            initNs={"owl": OWL},
        )

        results = []
        for row in g.query(query):
            herbName = [herb["name"] for herb in results]
            if str(row["name"]) not in herbName:
                synonymQuery = """
                    PREFIX onto: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

                    SELECT ?synonym ?name
                    WHERE {
                        
                        ?herb onto:hasName ?name .
                        ?herb onto:hasSynonym ?synonym .
                        OPTIONAL { ?herb onto:hasSynonym ?synonym }
                        FILTER (?name = "%s")
                    }
                    """ % str(
                    row["name"]
                )
                result_synonym = g.query(synonymQuery)
                synonymList = [syn["synonym"] for syn in result_synonym]

                otherNameQuery = """
                    PREFIX onto: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

                    SELECT ?otherName ?name
                    WHERE {
                        ?herb onto:hasName ?name .
                        ?herb onto:hasOtherName ?otherName .
                        OPTIONAL { ?herb onto:hasOtherName ?otherName }
                        FILTER (?name = "%s")
                    }
                    """ % str(
                    row["name"]
                )
                result_other_name = g.query(otherNameQuery)
                otherNameList = [oth["otherName"] for oth in result_other_name]
                
            name = str(row["name"])
            urlpicture = str(row["urlpicture"])
            other_name = otherNameList
            synonyms = synonymList
            binomial_name = str(row["binomialName"])
            family = str(row["family"])
            english_name = str(row["englishName"])
            pharmacology = str(row["pharmacology"])
            origin = str(row["origin"])
            character = str(row["character"])
            properties = str(row["properties"])
            genus_name = str(row["genusName"])
            specific_name = str(row["specificName"])
            ecology = str(row["ecology"])
            toxicology = str(row["toxicology"])
            chemical = str(row["chemical"])
            how_to_use = str(row["howToUse"])
            reference = str(row["reference"])

            for result in results:
                if result["name"] == name:
                    result["urlpicture"].append(urlpicture)
                    break
            else:  # if not found
                result_dict = {
                    "name": name,
                    "urlpicture": [urlpicture],
                    "otherName": [other_name],
                    "synonyms": [synonyms],
                    "binomialName": [binomial_name],
                    "family": [family],
                    "englishName": [english_name],
                    "pharmacology": [pharmacology],
                    "origin": [origin],
                    "properties": [properties],
                    "genusName": [genus_name],
                    "specificName": [specific_name],
                    "ecology": [ecology],
                    "chemical": [chemical],
                    "toxicology": [toxicology],
                    "howToUse": [how_to_use],
                    "reference": [reference],
                    "character": [character],
                }
                results.append(result_dict)

        return jsonify({"origins": results})
    except KeyError:
        return jsonify({"error": "Invalid JSON data"}), 400
    except Exception as e:
        print("Error executing SPARQL query:", e)
        return jsonify({"error": str(e)}), 500



@app.route("/system", methods=["POST"])
def system():
    systemName = request.json["name"]
    try:
        # Prepare SPARQL query
        query = prepareQuery(
            f"""
            SELECT ?name ?otherName ?synonym ?binomialName ?family ?englishName ?pharmacology ?origin ?character ?properties ?urlpicture ?genusName ?specificName ?ecology ?chemical ?toxicology ?howToUse ?reference
            WHERE {{
                ?herb <http://www.w3.org/2002/07/owl#isInSystem> <http://www.w3.org/2002/07/owl#{systemName}> .
                ?herb <http://www.w3.org/2002/07/owl#hasName> ?name .
                ?herb <http://www.w3.org/2002/07/owl#UrlPicture> ?urlpicture .
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasOtherName> ?otherName . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasSynonym> ?synonym . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasBinomialName> ?binomialName . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasFamily> ?family . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasEnglishName> ?englishName . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasPharmacology> ?pharmacology . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#Origin> ?origin . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasCharacter> ?character . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasProperties> ?properties . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasGenusName> ?genusName . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasSpecificName> ?specificName . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasEcology> ?ecology . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasToxicology> ?toxicology . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasChemical> ?chemical . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#hasHowToUse> ?howToUse . }}
                OPTIONAL {{ ?herb <http://www.w3.org/2002/07/owl#Reference> ?reference . }}
            }}
        """,
            initNs={"owl": OWL},
        )

        results = []
        for row in g.query(query):
            herbName = [herb["name"] for herb in results]
            if str(row["name"]) not in herbName:
                synonymQuery = """
                    PREFIX onto: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

                    SELECT ?synonym ?name
                    WHERE {
                        
                        ?herb onto:hasName ?name .
                        ?herb onto:hasSynonym ?synonym .
                        OPTIONAL { ?herb onto:hasSynonym ?synonym }
                        FILTER (?name = "%s")
                    }
                    """ % str(
                    row["name"]
                )
                result_synonym = g.query(synonymQuery)
                synonymList = [syn["synonym"] for syn in result_synonym]

                otherNameQuery = """
                    PREFIX onto: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

                    SELECT ?otherName ?name
                    WHERE {
                        ?herb onto:hasName ?name .
                        ?herb onto:hasOtherName ?otherName .
                        OPTIONAL { ?herb onto:hasOtherName ?otherName }
                        FILTER (?name = "%s")
                    }
                    """ % str(
                    row["name"]
                )
                result_other_name = g.query(otherNameQuery)
                otherNameList = [oth["otherName"] for oth in result_other_name]
                
            name = str(row["name"])
            urlpicture = str(row["urlpicture"])
            other_name = otherNameList
            synonyms = synonymList
            binomial_name = str(row["binomialName"])
            family = str(row["family"])
            english_name = str(row["englishName"])
            pharmacology = str(row["pharmacology"])
            origin = str(row["origin"])
            character = str(row["character"])
            properties = str(row["properties"])
            genus_name = str(row["genusName"])
            specific_name = str(row["specificName"])
            ecology = str(row["ecology"])
            toxicology = str(row["toxicology"])
            chemical = str(row["chemical"])
            how_to_use = str(row["howToUse"])
            reference = str(row["reference"])

            for result in results:
                if result["name"] == name:
                    result["urlpicture"].append(urlpicture)
                    break
            else:  # if not found
                result_dict = {
                    "name": name,
                    "urlpicture": [urlpicture],
                    "otherName": [other_name],
                    "synonyms": [synonyms],
                    "binomialName": [binomial_name],
                    "family": [family],
                    "englishName": [english_name],
                    "pharmacology": [pharmacology],
                    "origin": [origin],
                    "properties": [properties],
                    "genusName": [genus_name],
                    "specificName": [specific_name],
                    "ecology": [ecology],
                    "chemical": [chemical],
                    "toxicology": [toxicology],
                    "howToUse": [how_to_use],
                    "reference": [reference],
                    "character": [character],
                }
                results.append(result_dict)

        return jsonify({"systems": results})
    except KeyError:
        return jsonify({"error": "Invalid JSON data"}), 400
    except Exception as e:
        print("Error executing SPARQL query:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/origin2", methods=["POST"])
def origin2():
    originName = request.json["name"]
    try:
        # Prepare SPARQL query
        query = prepareQuery(
            f"""
            SELECT ?name ?urlpicture ?otherName
            WHERE {{
                ?herb <http://www.w3.org/2002/07/owl#isInOrigin> <http://www.w3.org/2002/07/owl#{originName}> .
                ?herb <http://www.w3.org/2002/07/owl#hasName> ?name .
                ?herb <http://www.w3.org/2002/07/owl#UrlPicture> ?urlpicture .
                ?herb <http://www.w3.org/2002/07/owl#hasOtherName> ?otherName .
            }}
        """,
            initNs={"owl": OWL},
        )

        results = []
        for row in g.query(query):
            name = str(row["name"])
            urlpicture = str(row["urlpicture"])
            otherName = str(row["otherName"])

            herb_names = [result["name"] for result in results]
            if name not in herb_names:
                result_dict = {
                    "name": name,
                    "urlpicture": [urlpicture],
                    "otherName": [otherName],
                }
                results.append(result_dict)
            else:

                for result in results:
                    if result["name"] == name:
                        result["urlpicture"].append(urlpicture)

        return jsonify({"origins": results})
    except Exception as e:
        print("Error executing SPARQL query:", e)
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/sparql2", methods=["POST"])
def sparql2():
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
              FILTER regex(?name, "%s", "i") .
            }
            LIMIT 5
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
