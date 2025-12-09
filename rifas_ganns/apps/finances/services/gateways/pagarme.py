import requests

url = "https://api.pagar.me/core/v5/customers"

payload = { "birthdate": "mm/dd/aaa" }
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Basic Z3VzdGF2b0BnbnBzaXN0ZW1hcy5jb20uYnI6Tm1jc2cxMjIhQEA="
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

class PagarmeHandler:
    def __init__(self, auth):
        self.auth = auth

    def create_customer(self, api_url, name, email, document, document_type, phones):
        payload = {
            name,
            email,
            document,
            document_type,
            phones
        }
        headers = self.request_headers_json()
        return self.post(headers, payload, api_url)

    def request_headers_json(self) -> dict:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self.auth
        }
        return headers
    
    def post(self, headers, payload, api_url):
        return requests.post(url=api_url, json=payload, headers=headers)