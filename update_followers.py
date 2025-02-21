import requests
import os

def update_followers():
    """
    Récupère les 10 derniers followers GitHub et met à jour la section correspondante du README.md
    avec leurs noms et avatars alignés.
    """
    username = "Julien-Quinodoz"
    url = f"https://api.github.com/users/{username}/followers?per_page=100"

    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Erreur lors de la récupération des followers. Code de statut: {response.status_code}")
        print("Détails:", response.json())
        return

    # Récupérer les données des followers
    followers = response.json()
    print(f"Réponse API: {followers}")  # Afficher la réponse de l'API pour le débogage

    # Filtrer les followers qui n'ont pas la clé 'created_at'
    followers = [follower for follower in followers if 'created_at' in follower]
    print(f"Followers après filtrage: {followers}")  # Afficher les followers après filtrage

    # Tri des followers par date de création, du plus récent au plus ancien
    followers = sorted(followers, key=lambda x: x['created_at'], reverse=True)

    # Récupérer les 10 derniers followers
    followers = followers[:10]

    # Construire la liste des followers à afficher dans le README
    followers_list = "\n".join([
        f"<tr><td><img src='https://github.com/{follower['login']}.png' width='50' height='50'></td>"
        f"<td><strong>{follower['login']}</strong></td><td><a href='{follower['html_url']}'>Profil</a></td></tr>"
        for follower in followers
    ])

    # Nouveau contenu à insérer dans le README
    new_section = f"""
## Derniers Followers GitHub

<table>
  <tr><th>Avatar</th><th>Nom d'utilisateur</th><th>Profil</th></tr>
  {followers_list}
</table>
"""

    # Chemin du fichier README.md
    readme_path = "README.md"

    # Vérifier si le fichier README.md existe
    if not os.path.exists(readme_path):
        print("❌ README.md introuvable.")
        return

    # Ouvrir et mettre à jour le README.md
    with open(readme_path, "r+") as file:
        content = file.read()

        # Si la section "Derniers Followers GitHub" existe déjà, on la remplace
        if "## Derniers Followers GitHub" in content:
            updated_content = content.split("## Derniers Followers GitHub")[0].rstrip() + "\n" + new_section
        else:
            # Sinon, on l'ajoute à la fin du fichier
            updated_content = content.strip() + "\n" + new_section

        # Réécrire le fichier README.md
        file.seek(0)
        file.write(updated_content)
        file.truncate()

    print("✅ README.md mis à jour avec les derniers followers.")

if __name__ == "__main__":
    update_followers()

