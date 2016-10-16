import requests

username='ebayk_hackgirl'
password='zd91pip2'
base_url='https://webapi.ebayclassifieds.com/webapi/'
import requests
import re
from requests.auth import HTTPBasicAuth
import logging
logger = logging.getLogger("iPoolLogger")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
import xml.etree.ElementTree
from xml.dom import minidom



def getEbayArticle():
	r=requests.get(base_url+'ads/', params={'q':'detox tea'},  auth=HTTPBasicAuth(username, password))
	logger.info(r.url)
	results=[]
	# r is an Response object; if you get <Response [200]> you're good
	# have a look at https://github.com/kennethreitz/requests
	if r.status_code<>200:
		##something went wrong ...
		logger.error("something went wrong {code}, {text}".format(code=r.status_code, text=r.text))
	else:
		print r.text
		#response=xml.etree.ElementTree.parse(r.text).getroot()
		xmldoc = minidom.parseString(r.text)
		#response= r.json()
		print xmldoc.getElementsByTagName('ad')
										
		
		
	return results

getEbayArticle()