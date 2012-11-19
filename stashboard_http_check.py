from stashboard_client import StashboardClient
import httplib
from urlparse import urlparse

class StashboardHttpCheck(StashboardClient):
    
    def __init__(self, configuration_key):
        super(StashboardHttpCheck, self).__init__()
        self.url,self.expected_status, self.service = self.load_configuration(configuration_key)
        
    def load_configuration(self, configuration_key):
        cfg = self.get_config()
        url = cfg.get(configuration_key, "url")
        status = int(cfg.get(configuration_key, "status"))
        service = cfg.get(configuration_key, "stashboard_service")
        return url, status, service
    
    def check(self):
        parsed_url = urlparse(self.url)
        connection = httplib.HTTPSConnection(parsed_url.netloc)
        if parsed_url == "https":
            connection = httplib.HTTPSConnection(parsed_url.netloc)
        connection.request("GET", self.url)
        status = connection.getresponse().status
        if status != self.expected_status:
            self.down(self.service)
        self.up(self.service)