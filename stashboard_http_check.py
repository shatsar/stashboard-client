from stashboard_client import StashboardClient
import httplib
from urlparse import urlparse
import ConfigParser
import ast
import time

class StashboardHttpCheck(StashboardClient):
    DEFAULT_RESPONSE_TIME_LIMIT = 10000
    
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
            
        try:
            self.response_time_limit = cfg.getint(configuration_key, "response_time")
        except ConfigParser.NoOptionError:
            self.response_time_limit = StashboardHttpCheck.DEFAULT_RESPONSE_TIME_LIMIT
    
    def check(self):
        parsed_url = urlparse(self.url)
        connection = httplib.HTTPConnection(parsed_url.netloc)
        if parsed_url.scheme == "https":
            connection = httplib.HTTPSConnection(parsed_url.netloc)
        try:
            connection.request("GET", self.url, headers=self.additional_headers)
            start = time.time()
            response = connection.getresponse()
            response_time_in_ms = (time.time() - start) * 1000
            if(response_time_in_ms > self.response_time_limit):
                self.warn(self.service)
                return
                
            status = int(response.status)
            if status != self.expected_status:
                self.down(self.service)
            else:
                self.up(self.service)
        except:
            self.down(self.service)