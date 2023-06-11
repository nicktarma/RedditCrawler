from flask import Flask, request, render_template
from sample import retrieve
# import logging, sys
# # logging.disable(sys.maxsize)
# #logging.basicConfig(level=logging.DEBUG)
import json

import lucene
import os
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser, MultiFieldQueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
from org.apache.lucene.search.similarities import BM25Similarity
from datetime import datetime
from org.apache.lucene.search import Sort, SortField


app = Flask(__name__)
 
 
 
 
@app.route('/', methods=['GET'])
def searchpage():
    return(render_template('searcharea.html'))



@app.route('/results', methods = ['POST', 'GET'])
def results():
    if request.method == 'GET':
        return f"Nothing"
    if request.method == 'POST':
        form_data = request.form
        query = form_data['query']
        print(f"this is the query: {query}")
        lucene.getVMEnv().attachCurrentThread()
        docs = retrieve('sample_lucene_index/', str(query))
        print(docs)

        return render_template('results.html',lucene_output = docs)



        # return render_template('results.html',lucene_output = {})
    

# lucene.initVM(vmargs=['-Djava.awt.headless=true'])

 
if __name__ == '__main__':
    app.run(debug=True)