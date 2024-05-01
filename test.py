from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

def parse_rdf_file(file_path):
    g = Graph()
    g.parse(file_path, format='xml')  # Assuming RDF file format is XML
    return g

def query_herbs_in_asia(graph):
    query = prepareQuery('''
        
            SELECT *
            WHERE {
              ?herb rdf:Description owl:Asia .
              
            }
            
    ''', initNs={"owl": "http://www.w3.org/2002/07/owl#", "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"})
    
    results = graph.query(query)
    for result in results:
        print(result)
    return [str(result.herbName) for result in results]

def main():
    rdf_file_path = 'SEAHERS_Ontology.rdf'  # Replace with the path to your RDF file
    graph = parse_rdf_file(rdf_file_path)
    asia_herb_names = query_herbs_in_asia(graph)
    print("Herb names originating in Asia:", asia_herb_names)

if __name__ == '__main__':
    main()
