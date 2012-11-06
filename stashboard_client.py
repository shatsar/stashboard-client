import oauth2
import json
import urllib
import ConfigParser

class StashboardClient:

	
	def __init__(self):
		consumer_key, consumer_secret = self.get_consumer_keys()
		oauth_key, oauth_secret = self.get_application_keys()
		self.client = StashboardClient.build_client(consumer_key, consumer_secret, oauth_key, oauth_secret)
		base_url = self.get_base_url()
		
		self.base_admin_url = "%s/admin/api/v1" % base_url
		pass;

	def up(self, service, message=None):
		if message is None:
			message = "up and running"
		self.post_event("up", service, message)
		
	def post_event(self, status, service, message):
		data = urllib.urlencode({
		    "status": status,
			"message": message
		})
		resp, content = self.client.request( self.base_admin_url + "/services/mashape/events", "POST", body=data)
		event = json.loads(content)
		print event
		
	def get_config(self):
		try:
			return self.cfg
		except AttributeError:
			self.cfg = ConfigParser.RawConfigParser()
			self.cfg.read("stashboard.cfg")
			return self.cfg
	
	def get_base_url(self):
		cfg = self.get_config()
		return cfg.get("stashboard", "base_url")
	
	def get_consumer_keys(self):
		cfg = self.get_config()
		return cfg.get("stashboard", "consumer_key"), cfg.get("stashboard", "consumer_secret") 
	
	def get_application_keys(self):
		cfg = self.get_config()
		return cfg.get("stashboard", "oauth_key"), cfg.get("stashboard", "oauth_secret") 
	
	@staticmethod	
	def build_client(consumer_key, consumer_secret, oauth_key, oauth_secret):
		consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
		token = oauth2.Token(oauth_key, oauth_secret)
		return oauth2.Client(consumer, token=token)		

v = StashboardClient()
v.up("mashape")