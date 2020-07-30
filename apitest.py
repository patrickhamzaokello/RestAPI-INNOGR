import requests
import json

reg = requests.get('https://innograpitest.herokuapp.com/apiposts/?format=json')

print(reg.json())