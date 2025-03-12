import requests
import os
import random

def update_followers():
    """
    Récupère les 36 derniers followers GitHub, mélange les cases et affiche un message interactif
    pour encourager les visiteurs à suivre le compte.
    """
    username = "Julien-Quinodoz"
    url = f"https://api.github.com/users/{username}/followers?per_page=36"

    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Erreur lors de la récupération des followers. Code de statut: {response.status_code}")
        print("Détails:", response.json())
        return

    followers = response.json()[::-1]  # Inverser pour afficher les derniers en premier

    # Compléter avec des cases "Your head here!" si moins de 36 followers
    total_cases = 36
    empty_cases_needed = total_cases - len(followers)

    empty_case_html = (
        "<td align='center' style='opacity:0.7;'>"
        "<a href='https://github.com/Julien-Quinodoz?tab=followers' target='_blank'>"
        "<img src='https://via.placeholder.com/50' width='50' height='50'><br>"
        "<strong>Your head here!</strong></a></td>"
    )

    cases = [
        (
            f"<td align='center'>"
            f"<img src='https://github.com/{follower['login']}.png' width='50' height='50'><br>"
            f"<strong>{follower['login']}</strong><br>"
            f"<a href='{follower['html_url']}'>Profil</a>"
            f"</td>"
        )
        for follower in followers
    ] + [empty_case_html] * empty_cases_needed  # Ajouter les cases vides

    # Mélanger toutes les cases
    random.shuffle(cases)

    # Générer le tableau avec 6 colonnes
    followers_list = ""
    columns = 6
    for i in range(0, total_cases, columns):
        row = "<tr>" + "".join(cases[i : i + columns]) + "</tr>\n"
        followers_list += row

    new_section = f"""
## Derniers Followers GitHub

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
