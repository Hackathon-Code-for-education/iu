from src.modules.providers.router import router as router_providers
from src.modules.user.router import router as router_users

routers = [
    router_providers,
    router_users,
]

__all__ = ["routers"]
