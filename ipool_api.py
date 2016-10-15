# You need to install the rauth module first with
# pip install rauth
# see https://rauth.readthedocs.org/en/latest/
#from rauth import OAuth1Session
import requests
import re
from requests.auth import HTTPBasicAuth
import logging
logger = logging.getLogger("iPoolLogger")
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
#fh = logging.FileHandler('spam.log')
#fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
# only consumer_key and consumer_secret needs to be defined 
#session = OAuth1Session(consumer_key='hackaton', consumer_secret='hackme')
# it's important to enable header based authentification, URL parameter signature will not work
# to ignore SSL certificate verify failed error by setting verify parameter to False

def getArticleFeed(keywords):
	r=requests.get('https://sandbox-api.ipool.asideas.de/sandbox/api/search', params={'q':keywords, 'types':'article','location':'Berlin'},  auth=HTTPBasicAuth('hackathon', 'hackme'))
	results=[]
	# r is an Response object; if you get <Response [200]> you're good
	# have a look at https://github.com/kennethreitz/requests
	if r.status_code<>200:
		##something went wrong ...
		logger.error("something went wrong {code}, {text}".format(code=r.status_code, text=r.text))
	else:
		response= r.json()
		print type(response["documents"])
		print len(response["documents"])
		docs=response["documents"]
		
		for d in docs:
			try:
				if re.search('en',d['language']):
					res={}
					for k,v in d.iteritems():
						if k in ['title', 'publishedUrl', 'keywords']:
							res.update({k:v})				  		
							##print k, '->',}(v) 
						if k == 'content':
							shortcut = v[:200]
							res.update({k:shortcut})
				results.append(res)
			except KeyError as k:	
				logger.error("key missing: {0}".format(k))
	return results

def nicePrintOut(results):
	if len(results)==0:
		print "Sorry, no articles found"
	else:
		for r in results:
			for k, v in r.iteritems():
				print k, "---->", v 

			print "\n"
			
			


keywords="female hygiene late period"
res=getArticleFeed(keywords)
nicePrintOut( res)																  

																  
																  
			