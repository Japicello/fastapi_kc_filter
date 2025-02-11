from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi_keycloak_middleware import KeycloakMiddleware
import re

class KeycloakFilterMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        keycloak_middleware: KeycloakMiddleware,
        exclude_patterns: list[str] = None
    ):
        super().__init__(app)
        self.keycloak_middleware = keycloak_middleware
        self.exclude_patterns = (
            [re.compile(pattern) for pattern in exclude_patterns]
            if exclude_patterns
            else []
        )

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # Si la ruta está excluida, omite Keycloak
        if any(pattern.fullmatch(path) for pattern in self.exclude_patterns):
            return await call_next(request)
        
        # Si no está excluida, aplica KeycloakMiddleware
        return await self.keycloak_middleware.dispatch(request, call_next)