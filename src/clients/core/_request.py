import logging
from datetime import datetime
from typing import Optional, Union, Dict, Any, Type, TypeVar
import aiohttp
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)
logger = logging.getLogger("uvicorn.error")


class RequestCore:
    def __init__(self, host: str):
        self.host = host.rstrip("/")

    def _get_headers(self, access_token: Optional[str] = None) -> Dict[str, str]:
        if not access_token:
            return None
        headers = {"Content-Type": "application/json"}
        headers["Authorization"] = f"Bearer {access_token}"
        return headers

    def _clean_payload(
        self, payload: Optional[Union[BaseModel, Dict[str, Any]]]
    ) -> Optional[Dict[str, Any]]:
        if payload is None:
            return None

        payload_dict = (
            payload.model_dump() if isinstance(payload, BaseModel) else payload.copy()
        )

        def _clean_value(value: Any) -> Any:
            if isinstance(value, datetime):
                return value.isoformat()
            elif isinstance(value, dict):
                return {k: _clean_value(v) for k, v in value.items() if v is not None}
            elif isinstance(value, list):
                return [_clean_value(v) for v in value if v is not None]
            return value

        return _clean_value(payload_dict)

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        access_token: Optional[str] = None,
        data: Optional[Union[BaseModel, Dict[str, Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[T]] = None,
    ) -> Union[T, Dict[str, Any], bool]:
        headers = self._get_headers(access_token)
        clean_data = self._clean_payload(data)
        clean_params = self._clean_payload(params)
        url = f"{self.host}/{endpoint.lstrip('/')}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method,
                    url,
                    headers=headers,
                    data=clean_data if not access_token else None,
                    json=clean_data if access_token else None,
                    params=clean_params,
                ) as response:
                    logger.info(f"Status: {response.status}")

                    if response.status >= 400:
                        error_text = await response.text()
                        logger.error(f"HTTP error: {response.status} - {error_text}")
                        return False

                    if response.status == 204:  # No Content
                        return True

                    response_data = await response.json()
                    return (
                        response_model(**response_data)
                        if response_model
                        else response_data
                    )

        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            return False

    async def get(
        self,
        endpoint: str,
        *,
        access_token: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[T]] = None,
    ) -> Union[T, Dict[str, Any], bool]:
        return await self._request(
            "GET",
            endpoint,
            access_token=access_token,
            params=params,
            response_model=response_model,
        )

    async def post(
        self,
        endpoint: str,
        *,
        access_token: Optional[str] = None,
        data: Optional[Union[BaseModel, Dict[str, Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[T]] = None,
    ) -> Union[T, Dict[str, Any], bool]:
        return await self._request(
            "POST",
            endpoint,
            access_token=access_token,
            data=data,
            params=params,
            response_model=response_model,
        )

    async def put(
        self,
        endpoint: str,
        *,
        access_token: Optional[str] = None,
        data: Optional[Union[BaseModel, Dict[str, Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[T]] = None,
    ) -> Union[T, Dict[str, Any], bool]:
        return await self._request(
            "PUT",
            endpoint,
            access_token=access_token,
            data=data,
            params=params,
            response_model=response_model,
        )

    async def delete(
        self,
        endpoint: str,
        *,
        access_token: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[T]] = None,
    ) -> Union[T, Dict[str, Any], bool]:
        return await self._request(
            "DELETE",
            endpoint,
            access_token=access_token,
            params=params,
            response_model=response_model,
        )
