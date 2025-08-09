import time
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import jwt  # PyJWT
from config import SECRET_KEY, ALGORITHM
import logging

logger = logging.getLogger(__name__)

class AuthMiddleware:
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        # Routes publiques qui ne nécessitent pas d'authentification
        if request.url.path in ["/auth/login", "/auth/token/refresh", "/docs", "/openapi.json", "/", "/health"]:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Token d'authentification manquant ou invalide"}
            )

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token expiré"}
            )
        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token invalide"}
            )

        return await call_next(request)