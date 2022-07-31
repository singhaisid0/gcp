from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from elasticsearchquerygenerator.elasticsearchquerygenerator import ElasticSearchQuery
from elasticsearch import Elasticsearch


cloudid = "ES_deployment_syndicate:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDgwZjUwNmIyMmYwOTRmYWQ4Yjk1NzE1YzIxMTEzZGIwJDBhZjM3OWE5ZGFlMTRjYmZhNjRkMDY3OTcwNDVlNDcy"
user = "elastic"
password = "t1ykTWNHHJY778GG5SasPrih"

es_client = Elasticsearch(cloud_id=cloudid, http_auth=(user, password))
app = Flask(__name__)
api = Api(app)

output = {}

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('q',help='Pass a sentence to analyse')



class Search_api(Resource):

    def get(self):

        # use parser and find the user's query
        args = parser.parse_args()
        sentence = args['q']
	
        query_input = sentence
        body = {
           "_source": ["Description"],
           "size": 20,
           "min_score": 0.6,
           "query": {
              "bool": {
                 "must": [],
                 "filter": [],
                 "should": [
                    
                    {
                       "multi_match": {
                             "query": query_input,
                             "type" : "cross_fields",
                             "fields" : ["Description"],
                             "operator" : "or"                    
                       }
                    }         
                 ]
              }
           }
        }
        return (es_client.search(index="south_africa_shows", body=body))

api.add_resource(Search_api, '/')

if __name__ == "__main__":
    app.run(debug=True)
