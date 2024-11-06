import requests

url = 'http://127.0.0.1:8000'
myobj = {'question': 'Qual classe voce recomendaria para quem está iniciando no DnD?'}

x = requests.post(url, json = myobj)

print(x.text)