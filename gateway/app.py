from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import httpx
from typing import Dict, Any
import os

app = FastAPI(title="EducAI Gateway Service")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À configurer en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration des services
SERVICES = {
    "auth": "http://localhost:8001",
    "user": "http://localhost:8002",
    "analytics": "http://localhost:8003",
    "recommender": "http://localhost:8004",
    "gamification": "http://localhost:8005",
    "chatbot": "http://localhost:8006"
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Client HTTP asynchrone
async_client = httpx.AsyncClient()

@app.on_event("shutdown")
async def shutdown_event():
    await async_client.aclose()

# Middleware pour la vérification du token
async def verify_token(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    try:
        async with async_client.get(
            f"{SERVICES['auth']}/api/token/verify",
            headers={"Authorization": f"Bearer {token}"}
        ) as response:
            if response.status_code == 200:
                return response.json()
            raise HTTPException(
                status_code=401,
                detail="Token invalide ou expiré"
            )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Erreur lors de la vérification du token"
        )

# Routes d'authentification
@app.post("/auth/login")
async def login(credentials: Dict[str, str]):
    async with async_client.post(
        f"{SERVICES['auth']}/api/login",
        json=credentials
    ) as response:
        return response.json()

@app.post("/auth/token/refresh")
async def refresh_token(refresh_token: Dict[str, str]):
    async with async_client.post(
        f"{SERVICES['auth']}/api/token/refresh",
        json=refresh_token
    ) as response:
        return response.json()

# Route pour le profil utilisateur
@app.get("/user/profile")
async def get_user_profile(user_data: Dict = Depends(verify_token)):
    user_id = user_data.get("user_id")
    async with async_client.get(
        f"{SERVICES['user']}/api/users/{user_id}",
        headers={"Authorization": f"Bearer {user_data['token']}"}
    ) as response:
        return response.json()

# Routes pour les statistiques
@app.get("/analytics/stats")
async def get_analytics(user_data: Dict = Depends(verify_token)):
    user_id = user_data.get("user_id")
    async with async_client.get(
        f"{SERVICES['analytics']}/api/stats/{user_id}",
        headers={"Authorization": f"Bearer {user_data['token']}"}
    ) as response:
        return response.json()

# Route pour les activités utilisateur
@app.get("/user/activities")
async def get_user_activities(user_data: Dict = Depends(verify_token)):
    user_id = user_data.get("user_id")
    async with async_client.get(
        f"{SERVICES['user']}/api/users/{user_id}/activities",
        headers={"Authorization": f"Bearer {user_data['token']}"}
    ) as response:
        return response.json()

# Route pour les recommandations
@app.get("/recommender/suggestions")
async def get_recommendations(user_data: Dict = Depends(verify_token)):
    user_id = user_data.get("user_id")
    async with async_client.get(
        f"{SERVICES['recommender']}/api/suggestions/{user_id}",
        headers={"Authorization": f"Bearer {user_data['token']}"}
    ) as response:
        return response.json()

# Route pour les achievements
@app.get("/gamification/achievements")
async def get_achievements(user_data: Dict = Depends(verify_token)):
    user_id = user_data.get("user_id")
    async with async_client.get(
        f"{SERVICES['gamification']}/api/achievements/{user_id}",
        headers={"Authorization": f"Bearer {user_data['token']}"}
    ) as response:
        return response.json()

# Route pour le chatbot
@app.post("/chatbot/message")
async def send_message(message: Dict[str, str], user_data: Dict = Depends(verify_token)):
    async with async_client.post(
        f"{SERVICES['chatbot']}/api/chat",
        json={**message, "user_id": user_data.get("user_id")},
        headers={"Authorization": f"Bearer {user_data['token']}"}
    ) as response:
        return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)