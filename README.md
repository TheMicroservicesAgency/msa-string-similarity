
# msa-string-similarity

Various algorithms to mesure the similarity of N strings.

Built with [Harry](https://github.com/rieck/harry), licensed under the GPLv3. From the Harry documentation :

> The tool supports several common distance and kernel functions for strings as well as some excotic similarity measures. The focus of Harry lies on implicit similarity measures, that is, comparison functions that do not give rise to an explicit vector space. Examples of such similarity measures are the Levenshtein distance, the Jaro-Winkler distance or the spectrum kernel.

## Quick start

Execute the microservice container with the following command :

    docker run -ti -p 9906:80 msagency/msa-string-similarity

## Examples

If no algorithm is specified, the program will use dist_levenshtein by default.
From wikipedia :

> In information theory and computer science, the Levenshtein distance is a string metric for measuring the difference between two sequences. Informally, the Levenshtein distance between two words is the minimum number of single-character edits (i.e. insertions, deletions or substitutions) required to change one word into the other.


    curl -XPOST 'localhost:9906/similarity' \
    -H 'Content-Type: application/json' \
    -d '[ "string1", "string2" ]'

    [[0.0, 1.0], [1.0, 0.0]]

The result is a matrix of the computed similarity values, in JSON.

To get the list of supported algorithms, get the /similarity/algorithms url :

    curl http://localhost:9906/similarity/algorithms

    {
      "algorithms": [
        {
          "algorithm": "kern_subsequence",
          "name": "Subsequence kernel",
          "reference": "Lodhi, Saunders, Shawe-Taylor, Cristianini, and Watkins...",
          "reference-url": "/similarity/references/kern_subsequence.pdf"
        },
        {
          "algorithm": "dist_damerau",
          "name": "Damerau-Levenshtein distance for strings",
          "reference": "Damerau. A technique for computer detection...",
          "reference-url": "/similarity/references/dist_damerau.pdf"
        },
      ...


To change the algorithm, just add the algorithm name as a parameter to the request :

    curl -XPOST 'localhost:9906/similarity?algorithm=dist_hamming' \
    -H 'Content-Type: application/json' \
    -d '[ "this is a string", "this is another string" ]'

    [[0.0, 12.0], [12.0, 0.0]]

Another example, but this time with the Jaro–Winkler distance and the granularity parameter. See [Bytes, Bits and Tokens](https://github.com/rieck/harry/blob/master/examples/TUTORIAL.md#bytes-bits-and-tokens) in the Harry documentation.

    curl -XPOST 'localhost:9906/similarity?algorithm=dist_jarowinkler&granularity=bits' \
    -H 'Content-Type: application/json' \
    -d '[ "this is a test string", "this is also a test string" ]'

    [[0.0, 0.0035714285913854837], [0.0035714285913854837, 0.0]]


## Endpoints

- [/similarity](/) : computes the similarity between N strings
- [/similarity/algorithms](/similarity/algorithms) : list the supported algorithms
- [/similarity/references/:algorithm](/similarity/references/dist_levenshtein.pdf) : documentation available for a given algorithm


## Standard endpoints

- [/ms/version](/ms/version) : returns the version number
- [/ms/name](/ms/name) : returns the name
- [/ms/readme.md](/ms/readme.md) : returns the readme (this file)
- [/ms/readme.html](/ms/readme.html) : returns the readme as html
- [/swagger/swagger.json](/swagger/swagger.json) : returns the swagger api documentation
- [/swagger/#/](/swagger/#/) : returns swagger-ui displaying the api documentation
- [/nginx/stats.json](/nginx/stats.json) : returns stats about Nginx
- [/nginx/stats.html](/nginx/stats.html) : returns a dashboard displaying the stats from Nginx

## About

A project by the [Microservices Agency](http://microservices.agency).
