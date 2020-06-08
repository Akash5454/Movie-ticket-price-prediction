import requests

url = 'http://localhost:5000/results'
r = requests.post(url,json={'city':'Lucknow', 'name':'INOX', 'seats':400, 'screens': 10, 'type':'Multiplex'})

print(r.json())