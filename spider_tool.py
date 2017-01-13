import requests
import argparse
import json


parser = argparse.ArgumentParser( description="spider remote control toos" )
parser.add_argument("scrapyd", default="localhost:6800", help="scrapyd remote address (localhost:6800)")
parser.add_argument("-projects", action="store_true", help="list available projects")
parser.add_argument("-jobs", action="store_true", help="list all jobs")
parser.add_argument("-spiders", action="store_true", help="list available spiders")
parser.add_argument("-crawl", nargs="+", dest="spider_arg", help="start spider")
parser.add_argument("-stop", nargs=1, dest="jobid", help="stop spider")
parser.add_argument("-items", nargs=2, help="get items by spider_name and jobid")
parser.add_argument("-logs", nargs=2, help="get logs by spider_name and jobid")
args = parser.parse_args()


if args.projects:
	data = json.loads( requests.get( "http://{netloc}{path}".format( netloc=args.scrapyd, path="/listprojects.json" ) ).content )
	print "projects:"
	for project in data["projects"]:
		print " {}".format(project)
elif args.jobs:
	params = {"project": "default"}
	data = json.loads( requests.get( "http://{netloc}{path}".format( netloc=args.scrapyd, path="/listjobs.json" ), params=params ).content )
	print "running:"
	for job in data['running']:
		print " spider: " + job["spider"]
		print " id: " + job["id"]
	print "finished:"
	for job in data['finished']:
		print " spider: " + job["spider"]
		print " id: " + job["id"]
elif args.spiders:
	params = {"project": "default"}
	data = json.loads( requests.get( "http://{netloc}{path}".format( netloc=args.scrapyd, path="/listspiders.json" ), params=params ).content ) 
	print "spiders:"
	for spider in data["spiders"]:
		print " {}".format(spider)
elif args.spider_arg:
	params = {"project": "default"}
	params.update( { "spider": args.spider_arg[0] } )
	for arg in args.spider_arg[1:]:
		params.update( { arg.split('=')[0]: arg.split('=')[1] } )
	data = json.loads( requests.post( "http://{netloc}{path}".format( netloc=args.scrapyd, path="/schedule.json" ), params=params ).content ) 
	print data["status"]
elif args.jobid:
	params = { "project": "default", "job": args.jobid[0] }
	data = json.loads( requests.post( "http://{netloc}{path}".format( netloc=args.scrapyd, path="/cancel.json"), params=params ).content ) 
	print data["status"]
elif args.items:
	spider = args.items[0]
	jobid = args.items[1]
	print requests.get( "http://{netloc}{path}".format( netloc=args.scrapyd, path="/items/default/" + spider + "/" + jobid + ".jl") ).content
elif args.logs:
	spider = args.logs[0]
	jobid = args.logs[1]
	print requests.get( "http://{netloc}{path}".format( netloc=args.scrapyd, path="/logs/default/" + spider + "/" + jobid + ".log") ).content