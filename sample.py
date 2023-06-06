import logging, sys
logging.disable(sys.maxsize)
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

sample_doc = [
    {
        'title' : 'A',
        'context' : 'lucene is a useful tool for searching and information retrieval'
    },
    {
        'title' : 'B',
        'context' : 'Bert is a deep learning transformer model for encoding textual data'
    },
    {
        'title' : 'C',
        'context' : 'Django is a python web framework for building backend web APIs'
    }
]

def create_index(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    store = SimpleFSDirectory(Paths.get(dir)) # Base class for Directory implementations that stores index files in the file system
    analyzer = StandardAnalyzer() # Filters tokens using a list of English stop words.
    config = IndexWriterConfig(analyzer) # Holds all the configuration that is used to crteate an IndexWriter()
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config) # The function that creates and maintains an index

    metaType = FieldType() # Describe the properties of a field
    metaType.setStored(True)
    metaType.setTokenized(False)

    contextType = FieldType()
    contextType.setStored(True)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    with open("data.json", 'r') as file:
        data = json.load(file)


    # i=0
    for post in data:
        
        # Counting the number of posts 
        # i+=1
        
        title = post.get('title')
        score = post.get('score')
        id = post.get('id')
        subreddit = post.get('subreddit')
        url = post.get('url')
        num_comments = post.get('num_comments')
        body = post.get('body')
        created = post.get('created')
        comments = post.get('comment_list')
        externTitles = post.get('externTitles')
        
        doc = Document()
        doc.add(Field('Title', str(title), contextType))
        doc.add(Field('Score', str(score), metaType))
        doc.add(Field('Id', str(id), metaType))
        doc.add(Field('Subreddit', str(subreddit), metaType))
        doc.add(Field('Url', str(url), metaType))
        doc.add(Field('Num_comments', str(num_comments), metaType))
        doc.add(Field('Body', str(body), contextType))
        doc.add(Field('Created', str(created), metaType))
        doc.add(Field('Comments', str(comments), contextType))
        doc.add(Field('ExternTitles', str(externTitles), metaType))
        
        writer.addDocument(doc)



    # for sample in sample_doc:
    #     title = sample['title']
    #     context = sample['context']
    #     doc = Document()
    #     doc.add(Field('Title', str(title), metaType))
    #     doc.add(Field('Context', str(context), contextType))
    #     writer.addDocument(doc)
    writer.close()


def retrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))

    fields_to_search = ["Title", "Body", "Comments"]
    parser = MultiFieldQueryParser(fields_to_search, StandardAnalyzer())
    parsed_query = parser.parse(query)

    topDocs = searcher.search(parsed_query, 10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "title": doc.get("Title"),
            # "body": doc.get("Body"),
            # "comments": doc.get("Comments"),
        })
    print(topkdocs)



# def retrieve(storedir, query):
#    searchDir = NIOFSDirectory(Paths.get(storedir)) # Uses java.nio's File Channel's positional io when reading to avoid synchronization when reading from the same file.
#    searcher = IndexSearcher(DirectoryReader.open(searchDir)) # Implements search over a single IndexReader

#    parser = QueryParser('Body', StandardAnalyzer()) # Creating a QueryParser to parse within a contextType field using analyzer a i.e. StandardAnalyzer()
#    parsed_query = parser.parse(query)

#    topDocs = searcher.search(parsed_query, 10).scoreDocs
#    topkdocs = []
#    for hit in topDocs:
#        doc = searcher.doc(hit.doc)
#        topkdocs.append({
#        "score": hit.score,
#        "text": doc.get("Body")
#        })
#    print(topkdocs)

lucene.initVM(vmargs=['-Djava.awt.headless=true']) # Initializes the necessary Java environments for lucene to work correctly
create_index('sample_lucene_index/')
retrieve('sample_lucene_index/','people')
