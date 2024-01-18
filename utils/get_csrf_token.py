import requests


# URL de l'application Django
url = 'http://127.0.0.1:8000/crm/login/'

# Effectue une requête GET pour obtenir le jeton CSRF
response = requests.get(url, headers={'Accept': 'application/json'})

# Imprime le contenu complet de la réponse
print(response.content)

# Imprime tous les en-têtes de la réponse
print(response.headers)

# Récupère le jeton CSRF à partir des cookies
csrf_token = response.cookies.get('csrftoken')

print(csrf_token)
