import requests
import os
import random

def follower_cell(follower):
    return (
        f"<td align='center'>"
        f"<img src='https://github.com/{follower['login']}.png' width='50' height='50'><br>"
        f"<strong>{follower['login']}</strong><br>"
        f"<a href='{follower['html_url']}'>Profil</a>"
        f"</td>"
    )

def fetch_all_followers(username):
    """Récupère toute la liste, du plus ancien au plus récent."""
    followers = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/followers?per_page=100&page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"❌ Erreur lors de la récupération des followers. Code de statut: {response.status_code}")
            print("Détails:", response.json())
            return None

        batch = response.json()
        if not isinstance(batch, list):
            print("❌ Réponse inattendue de l'API followers.")
            return None

        followers.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    return followers

def update_followers():
    """
    Écrit les 6 derniers abonnés, puis la grille des 36 premiers followers
    de l'API, mélangée, avec des cases vides s'il en manque.
    """
    username = "Julien-Quinodoz"
    all_followers = fetch_all_followers(username)
    if all_followers is None:
        return

    # Fin de liste API = plus récents. Affichés du plus récent au plus ancien.
    latest = list(reversed(all_followers[-6:]))
    latest_row = "<tr>" + "".join(follower_cell(follower) for follower in latest) + "</tr>\n"

    # Grille existante : même source (36 premiers) puis mélange.
    followers = all_followers[:36][::-1]

    # Compléter avec des cases "Your head here!" si moins de 36 followers
    total_cases = 36
    empty_cases_needed = total_cases - len(followers)

    # URL du GIF pour "Your head here!"
    empty_case_html = (
        "<td align='center' style='opacity:0.7;'>"
        "<a href='https://github.com/Julien-Quinodoz?tab=followers' target='_blank'>"
        "<img src='https://drive.google.com/uc?id=1MabxgCT39On1bnoQ-4huFuiWVSRWUPPS' width='50' height='50'><br>"
        "<strong>Your head here!</strong></a></td>"
    )

    cases = [follower_cell(follower) for follower in followers] + [empty_case_html] * empty_cases_needed

    # Mélanger toutes les cases
    random.shuffle(cases)

    # Générer le tableau avec 6 colonnes
    followers_list = ""
    columns = 6
    for i in range(0, total_cases, columns):
        row = "<tr>" + "".join(cases[i : i + columns]) + "</tr>\n"
        followers_list += row

    new_section = f"""
## Derniers Followers GitHub (Màj à 23h42)

### 6 derniers abonnés

<table>
  {latest_row}
</table>

<table>
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
