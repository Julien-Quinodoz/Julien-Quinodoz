import requests
import os

def update_followers():
    """
    Récupère les 10 derniers followers GitHub et met à jour la section correspondante du README.md
    avec leurs noms et avatars alignés.
    """
    username = "Julien-Quinodoz"
    url = f"https://api.github.com/users/{username}/followers?per_page=10"

    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Erreur lors de la récupération des followers. Code de statut: {response.status_code}")
        print("Détails:", response.json())
        return

    followers = response.json()[::-1]  # Inverser pour afficher les derniers en premier
    followers_list = "\n".join([
        f"<tr><td><img src='https://github.com/{follower['login']}.png' width='50' height='50'></td>"
        f"<td><strong>{follower['login']}</strong></td><td><a href='{follower['html_url']}'>Profil</a></td></tr>"
        for i, follower in enumerate(followers)
    ])

    new_section = f"""
## Derniers Followers GitHub

<table>
  <tr><th>Avatar</th><th>Nom d'utilisateur</th><th>Profil</th></tr>
  {followers_list}
</table>
"""

    readme_path = "README.md"

    if not os.path.exists(readme_path):
        print("❌ README.md introuvable.")
        return

    with open(readme_path, "r+") as file:
        content = file.read()

        if "## Derniers Followers GitHub" in content:
            updated_content = content.split("## Derniers Followers GitHub")[0].rstrip() + "\n" + new_section
        else:
            updated_content = content.strip() + "\n" + new_section

        file.seek(0)
        file.write(updated_content)
        file.truncate()

    print("✅ README.md mis à jour avec les derniers followers.")

if __name__ == "__main__":
    update_followers()
