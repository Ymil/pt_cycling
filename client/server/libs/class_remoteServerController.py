import requests
import json
class remoteServerController:
    def put(self, data):
        url = "{}/{}".format(self.server, data)
        response = requests.put(url).text
        if(len(response)):
            try:
                response = json.loads(response)
            except:
                pass
        return response
    
    def get(self, data):
        url = "{}/{}".format(self.server, data)
        response = requests.get(url).text
        if(len(response)):
            response = json.loads(response)
        return response
        