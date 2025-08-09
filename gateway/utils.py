import logging
from typing import Dict, Any, Optional
from fastapi import HTTPException
import httpx
from config import HTTP_TIMEOUT, MAX_RETRIES, LOG_LEVEL, LOG_FORMAT

# Configuration du logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class ServiceClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=HTTP_TIMEOUT,
            limits=httpx.Limits(max_retries=MAX_RETRIES)
        )

    async def close(self):
        await self.client.aclose()

    async def _make_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            response = await self.client.request(
                method=method,
                url=url,
                headers=headers,
                json=json
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=str(e)
            )
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail="Service temporairement indisponible"
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Erreur interne du serveur"
            )

    async def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return await self._make_request("GET", url, headers=headers)

    async def post(self, url: str, json: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return await self._make_request("POST", url, headers=headers, json=json)

    async def put(self, url: str, json: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return await self._make_request("PUT", url, headers=headers, json=json)

    async def delete(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return await self._make_request("DELETE", url, headers=headers)