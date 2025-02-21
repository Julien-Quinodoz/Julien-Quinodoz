import requests
import os

# Remplacer par ton nom d'utilisateur GitHub
username = "Julien-Quinodoz"
url = f"https://api.github.com/users/{username}/followers?per_page=10"

# Faire une requête pour obtenir les followers
response = requests.get(url)
followers = response.json()

# Générer la liste des derniers followers
followers_list = "\n".join([f"{i+1}. [{follower['login']}]({follower['html_url']})" for i, follower in enumerate(followers)])

# Préparer le contenu Markdown pour le README
readme_content = f"""
## Derniers Followers GitHub

{followers_list}
"""

# Mettre à jour le fichier README.md
with open("README.md", "r", encoding="utf-8") as file:
    readme = file.readlines()

# Chercher la section où les followers doivent être insérés
start_index = None
end_index = None
for i, line in enumerate(readme):
    if "## Derniers Followers GitHub" in line:
        start_index = i
        break

# Si la section est trouvée, on la remplace, sinon on l'ajoute
if start_index is not None:
    end_index = start_index + 1
    while end_index < len(readme) and readme[end_index].strip() != "":
        end_index += 1
    readme = readme[:start_index + 1] + [followers_list + "\n"] + readme[end_index:]
else:
    readme.append(f"\n## Derniers Followers GitHub\n\n{followers_list}\n")

# Sauvegarder les modifications dans le README.md
with open("README.md", "w", encoding="utf-8") as file:
    file.writelines(readme)

print("Le fichier README.md a été mis à jour avec les 10 derniers followers.")
