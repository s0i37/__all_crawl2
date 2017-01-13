# -*- coding: utf-8 -*-
import json
from requests import get, post, put, delete
from elasticsearch import Elasticsearch
from sys import argv, stdout
import argparse
import base64, re

RED = "\x1b[1;31m"
GREEN_NORM = "\x1b[0;32m"
GREEN_MARK = "\x1b[0;42m"
YELLOW = "\x1b[4;33m"
BLUE = "\x1b[0;34m"
CYAN = "\x1b[0;36m"
RESET = "\x1b[0m"


parser = argparse.ArgumentParser( description='search machine control tool' )
parser.add_argument("elasticsearch", type=str, default="localhost:9200", help="elasticsearch address (localhost:9200)")
parser.add_argument("-init", action="store_true", help="init index")
parser.add_argument("-query", nargs="+", help="search query")
parser.add_argument("-import", dest="jsonlines_file", help="import data")
parser.add_argument("-drop", action="store_true", help="drop index")
parser.add_argument("-backup", type=str, dest="location", help="backup index")
parser.add_argument("-restore", type=str, dest="backup_location", help="restore index")
parser.add_argument("-stop", action="store_true", help="close index")
parser.add_argument("-start", action="store_true", help="open index")
parser.add_argument("-autocomplete", action="store_true", help="enable autocomplete")
parser.add_argument("-o", "--offset", type=int, help="offset results in query")
parser.add_argument("-c", "--count", type=int, help="count results in query")
parser.add_argument("-i", "--index", type=str, help="index where to search", default="")
args = parser.parse_args()

SETTINGS = {
	"mappings": {
		"page": {
			"_source" : {"enabled" : True},
			"properties":{
				"inurl": {
					"type": "string"
				},
				"site": {
					"type": "string",
					"index": "not_analyzed"
				},
				"ext": {
					"type": "string",
					"index": "not_analyzed"
				},
				"intitle": {
					"type": "string"
				},
				"intext": {
					"type": "string"
				},
				"filetype": {
					"type": "string",
					"index": "not_analyzed"
				}
			},
			"_timestamp": {
				"enabled":True
			}
		}
	},
	"settings": {
		"analysis": {
			"filter": {
				"russian_stop": {
					"type": "stop",
					"stopwords": "_russian_"
				}
			},
			"analyzer": {
				"russian": {
					"type": "custom",
					"filter": ["lowercase", "russian_morphology", "russian_stop"],
					"tokenizer": "standard"
				}
			}
		}
	}
}

SETTINGS_AUTOCOMPLETE = {
	"analysis": {
		"filter": {
			"autocomplete_filter": {
				"type": "edge_ngram",
				"min_gram": 1,
				"max_gram": 20
			}
		},
		"analyzer": {
			"autocomplete": {
				"type": "custom",
				"tokenizer": "standard",
				"filter": ["lowercase", "autocomplete_filter", "russian_morphology", "russian_stop"]
			}
		}
	}
}

QUERY = {
	"from": args.offset or 0,
	"size": args.count or 10,
	"query": {
		#"simple_query_string": {
		#"multi_match": {
		"query_string": {
			"query": '',
			"fields": ["inurl^100","intitle^50","intext^5"],
			"default_operator": "AND",
			"fuzziness": "AUTO",
			"analyzer": "russian",
		}
	},
	"highlight": {
		"order": "score",
		"fields": {
			"*": {
				"pre_tags" : [ GREEN_MARK ],
				"post_tags" : [ GREEN_NORM ],
				"fragment_size": 50,
				"number_of_fragments": 3
			}
		}
	}
}

REPOSITORY = {
	"type":"fs",
	"settings":{
		"location": "",
		"compress":True
	}
}

def init_index(index):
	print post( "http://{netloc}/{index}".format( netloc=args.elasticsearch, index=index ), data=json.dumps(SETTINGS) ).content

def drop_index(index):
	print delete( "http://{netloc}/{index}".format( netloc=args.elasticsearch, index=index ) ).content

# echo 'path.repo: ["/opt/elasticsearch-2.3.5/backup/"]' >> /opt/elasticsearch-2.3.5/config/elasticsearch.yml
def backup_index(location, index):
	print put( "http://{netloc}/_snapshot/backup/".format( netloc=args.elasticsearch ), data=json.dumps(REPOSITORY) ).content
	print put( "http://{netloc}/_snapshot/backup/{location}?wait_for_completion=true".format( netloc=args.elasticsearch, location=location ), data=json.dumps( {"indices": index} ) ).content

def restore_index(location):
	print post( "http://{netloc}/_snapshot/backup/{location}/_restore?wait_for_completion=true".format( netloc=args.elasticsearch, location=location ) ).content

def print_mapping_and_settings(index):
	print get( "http://{netloc}/{index}/_mapping?pretty".format( netloc=args.elasticsearch, index=index ) ).content
	print get( "http://{netloc}/{index}/_settings?pretty".format( netloc=args.elasticsearch, index=index ) ).content

def print_indices():
	print get('http://{netloc}/_cat/indices?v'.format( netloc=args.elasticsearch ) ).content

def stop(index):
	print post( "http://{netloc}/{index}/_close".format( netloc=args.elasticsearch, index=index ) ).content

def start(index):
	print post( "http://{netloc}/{index}/_open".format( netloc=args.elasticsearch, index=index ) ).content

def autocomplete(index):
	print put( "http://{netloc}/{index}/_settings".format( netloc=args.elasticsearch, index=index ), data=json.dumps(SETTINGS_AUTOCOMPLETE) ).content

if args.init:
	init_index(args.index)

elif args.drop:
	drop_index(args.index)

elif args.jsonlines_file:
	if len(argv) < 3:
		print_help( argv[0] )
		exit()

	es = Elasticsearch( [args.elasticsearch] )
	with open( args.jsonlines_file, 'r' ) as f:
		while True:
			line = f.readline()
			if not line:
				break
			page = json.loads(line)
			print page["inurl"]
			es.index( index=args.index, doc_type='page', id=re.sub( r'[\n/]', '', base64.encodestring( page["inurl"] ) ), body=page )

elif args.query:
	QUERY['query']['query_string']['query'] = ' '.join( args.query )
	es = Elasticsearch( [args.elasticsearch] )
	results = es.search( index=args.index, body=QUERY )
	found = results['hits']['total']
	print '{color}found: {found}'.format( found=found, color=BLUE )
	for result in results['hits']['hits']:
		score = result['_score']
		url = result['_source']['inurl']
		title = result['_source']['intitle']
		texts = ''
		for text in result['_source'].values():
			texts += text
		matches = []
		for match in result['highlight'].values():
			matches += match
		stdout.write( '{color}{title}\n'.format( color=RED, title=title.encode('utf-8') ) )
		stdout.write( u'{color}{url} {_color}({score})\n'.format( score=score, url=url, color=YELLOW, _color=BLUE ) )
		stdout.write( '{color}{text}\n\n'.format( text= " ... ".join( matches ).encode('utf-8'), color=GREEN_NORM ) )
		stdout.write( RESET )
	print '{color}show {show}/{found}'.format( show=(args.count or 10)+(args.offset or 0), found=found, color=CYAN )

elif args.location:
	REPOSITORY["settings"]["location"] = args.location
	backup_index(args.location, args.index)

elif args.backup_location:
	restore_index(args.backup_location)

elif args.stop:
	stop(args.index)

elif args.start:
	start(args.index)

elif args.autocomplete:
	autocomplete(args.index)

else:
	if args.index:
		print_mapping_and_settings(args.index)
	else:
		print_indices()


#curl "http://lo:9200/_analyze?pretty&analyzer=russian&text=%D0%92%D0%B5%D1%81%D0%B5
#curl -XDELETE http://lo:9200/_snapshot/my_backup
