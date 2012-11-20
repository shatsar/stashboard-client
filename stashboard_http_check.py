from stashboard_client import StashboardClient
import httplib
from urlparse import urlparse
import ConfigParser
import ast

class StashboardHttpCheck(StashboardClient):
    
    def __init__(self, configuration_key):
        super(StashboardHttpCheck, self).__init__()
        self.load_configuration(configuration_key)
        
    def load_configuration(self, configuration_key):
        cfg = self.get_config()
        self.url = cfg.get(configuration_key, "url")
        self.expected_status = cfg.getint(configuration_key, "status")
        self.service = cfg.get(configuration_key, "stashboard_service")
        try:
            self.additional_headers = ast.literal_eval(cfg.get(configuration_key, "header"))
        except ConfigParser.NoOptionError:
            self.additional_headers = {}
    
    def check(self):
        parsed_url = urlparse(self.url)
        connection = httplib.HTTPConnection(parsed_url.netloc)
        if parsed_url.scheme == "https":
            connection = httplib.HTTPSConnection(parsed_url.netloc)
        connection.request("GET", self.url, headers=self.additional_headers)
        response = connection.getresponse()
        status = int(response.status)
        if status != self.expected_status:
            self.down(self.service)
        else:
            self.up(self.service)