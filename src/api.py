import requests


class ApiClient:
    def __init__(self, url):
        self.url = url

    def get(self, path):
        response = requests.get('%s%s' % (self.url, path))

        return response.json()

    def get_system(self, system_id):
        return self.get('/api/v1/systems/%s' % system_id)
