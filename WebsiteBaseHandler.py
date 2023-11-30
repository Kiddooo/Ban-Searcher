import requests
import json
from tqdm import tqdm

class BaseHandler:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
        self.FLARESOLVER_URL = 'http://localhost:8191/v1'


    def get_response(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=60, allow_redirects=False)
            if response.status_code == 200:
                return response.text
        except requests.exceptions.RequestException as e:
            tqdm.write(str(e) + url)
            return None

    def parse_website_html(self, response_text, url):
        raise NotImplementedError

    def handle_request(self, url):
        response_text = self.get_response(url)
        if response_text is not None:
            return self.parse_website_html(response_text, url)
        
    def get_flaresolverr_response(self, url):
        try:
            headers = {'Content-Type': 'application/json'}
            data = {"cmd": "request.get", "url": f"{url}", "maxTimeout": 60000}
            response = requests.post(self.FLARESOLVER_URL, data=json.dumps(data), headers=headers, timeout=60, allow_redirects=False).json()
            if response.get('solution').get('status') == 200:
                return response.get('solution').get('response')
        
        except requests.exceptions.RequestException as e:
            tqdm.write(str(e) + url)
            return None
    
    def handle_flaresolverr_request(self, url):
        response_text = self.get_flaresolverr_response(url)
        if response_text is not None:
            return response_text