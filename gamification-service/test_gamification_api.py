import requests

BASE_URL = "http://127.0.0.1:8000/api/gamification/"
USERNAME = "educuser@gmail.com"  # 🔁 Remplace par ton nom d’utilisateur
PASSWORD = "educuser@gmail.com"  # 🔁 Remplace par ton mot de passe

# Étape 1 – Obtenir le token JWT
def get_token():
    url = BASE_URL + "token/"
    response = requests.post(url, json={"username": USERNAME, "password": PASSWORD})
    data = response.json()
    return data.get("access")

# Étape 2 – Mettre à jour le score
def update_score(token, user_id, points):
    url = BASE_URL + "score/update/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json={"user_id": user_id, "points": points}, headers=headers)
    print("🧪 update_score:", response.status_code, response.json())

# Étape 3 – Voir le score
def get_score(token, user_id):
    url = BASE_URL + f"score/{user_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print("📊 get_score:", response.status_code, response.json())

# Étape 4 – Voir les badges
def get_badges(token, user_id):
    url = BASE_URL + f"badges/{user_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print("🏅 get_badges:", response.status_code, response.json())

# Lancer les tests
if __name__ == "__main__":
    user_id = 1       # 🔁 Ton ID utilisateur
    points_to_add = 10

    token = get_token()
    if token:
        update_score(token, user_id, points_to_add)
        get_score(token, user_id)
        get_badges(token, user_id)
    else:
        print("❌ Échec d'authentification")
