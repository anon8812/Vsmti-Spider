import urllib2, ConfigParser
from vsmtispider import log

config = ConfigParser.ConfigParser()
config.read('config.ini')

class Facebook:
	def __init__(self):
		self.appID = config.get('Facebook', 'Application ID')
		self.apiKEY = config.get('Facebook', 'API Key')
		self.apiSEC = config.get('Facebook', 'API Secret')
		self.pageUID = config.get('Facebook', 'Page UID')
		log.write('Fetching token from Facebook:')
		self.token = self.get_token()
		log.write(self.token)
		
	def get_token(self):
		fbstream = urllib2.urlopen('https://graph.facebook.com/oauth/access_token?client_id=' + self.appID + '&grant_type=client_credentials&client_secret=' + self.apiSEC)
		return fbstream.read()
		
	def publish(self, story):
		datastream = urllib2.urlopen('https://api.facebook.com/method/stream.publish?message=' + story[0].encode('utf-8', 'replace').replace(' ', '%20') + '%0A' + story[1].encode('utf-8', 'replace').replace(' ', '%20') + '&uid=' + self.pageUID + '&' + self.token)
		log.write('New post published')
		
	def publish_link(self, story):
		datastream = urllib2.urlopen('https://api.facebook.com/method/stream.publish?message=' + story[0].encode('utf-8', 'replace').replace(' ', '%20') + '%0A' + story[1].encode('utf-8', 'replace').replace(' ', '%20') + '&action_links=[{"text":"Link","href":"' + story[3].encode('utf-8', 'replace') + '"}]&uid=' + self.pageUID + '&' + self.token)
		log.write('New post published')