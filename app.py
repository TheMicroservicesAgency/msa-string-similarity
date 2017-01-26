from flask import Flask, request, jsonify, send_from_directory
import harry
import numpy
import random
import json
import logging

# disable the warnings
logging.getLogger("harry").setLevel(logging.ERROR)

app = Flask(__name__)

# load the list of supported algorithms in memory
algorithms = []
with open('data/algorithms.json') as f:
    content = f.read()
    algorithms = json.loads(str(content))

supported_algorithms = []
for algo in algorithms['algorithms']:
    supported_algorithms.append(algo['algorithm'])

# for the now supported granularity if hardcoded
supported_granularity = ["bits", "bytes", "tokens"]

# add the caching headers
@app.after_request
def add_header(response):
    response.cache_control.max_age = 31536000
    response.cache_control.public = True
    return response

# return the list of algorithms
@app.route('/similarity/algorithms')
def return_algorithms():
  response = jsonify(algorithms)
  return response


# serve the doc for a given algorithm
@app.route('/similarity/references/<algorithm>')
def return_reference(algorithm):
  response = send_from_directory('data/references/', algorithm)
  return response


# the actual service, expects a HTTP POST with a JSON document
# containing a list of strings, will compare the strings and return
# the results as a matrix, also in JSON
@app.route('/similarity' , methods=['POST'])
def compare_strings():

    # for a more detailed explanation for of the parameters
    # see http://mlsec.org/harry/tutorial.html
    algorithm = "dist_levenshtein"
    granularity = "bytes"
    tokens_delimiter = ""

    # change the default algorithm if another one is specified
    arg_algorithm = request.args.get("algorithm")
    if arg_algorithm:
        if arg_algorithm in supported_algorithms:
            algorithm = arg_algorithm
        else:
            msg = "%s is not a supported algorithm. " % arg_algorithm
            msg += "Only %s are supported." % supported_algorithms
            msg = msg.replace('\'', '')
            response = "{\"ERROR\" : \"%s\"}" % msg
            return response, 400

    # use the granularity parameter if it's specified
    arg_granularity = request.args.get("granularity")
    if arg_granularity:
        if arg_granularity in supported_granularity:
            granularity = arg_granularity
        else:
            msg = "%s is not a supported granularity. " % arg_granularity
            msg += "Only %s are supported." % supported_granularity
            msg = msg.replace('\'', '')
            response = "{\"ERROR\" : \"%s\"}" % msg
            return response, 400

    # if the granularity is 'tokens', also check for the delimiter parameter
    arg_delimiter = request.args.get("delimiter")
    if arg_delimiter:
        if granularity == "tokens":
            tokens_delimiter = arg_delimiter
        else:
            msg = "The granularity parameter must be tokens for the"
            msg += " delimiter to be used."
            response = "{\"ERROR\" : \"%s\"}" % msg
            return response, 400

    strings = request.json

    results = []
    if granularity == "tokens" and tokens_delimiter != "":
        results = harry.compare(strings, measure=algorithm,
                                         granularity=granularity,
                                         token_delim=tokens_delimiter)
    else:
        results = harry.compare(strings, measure=algorithm,
                                         granularity=granularity)

    response = json.dumps(results.tolist())
    return response


if __name__ == "__main__":

    app.run(port=8080, threaded=True)
