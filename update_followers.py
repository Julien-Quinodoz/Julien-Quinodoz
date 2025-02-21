import requests

# Remplacer par ton nom d'utilisateur GitHub
username = "ton_utilisateur"
url = f"https://api.github.com/users/{username}/followers?per_page=10"

# Faire une requête pour obtenir les followers
response = requests.get(url)
followers = response.json()

# Vérifier si la réponse est correcte
if response.status_code != 200:
    print("Erreur lors de la récupération des followers.")
else:
    # Générer la liste des derniers followers avec leurs noms et liens GitHub
    followers_list = "\n".join([f"{i+1}. [{follower['login']}]({follower['html_url']})" for i, follower in enumerate(followers)])

    # Préparer le contenu Markdown pour le README
    readme_content = f"""
## Derniers Followers GitHub

{followers_list}
"""

    # Afficher le contenu pour vérifier
    print(readme_content)
