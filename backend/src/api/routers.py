from src.modules.providers.router import router as router_providers
from src.modules.user.router import router as router_users
from src.modules.files.router import router as router_files
from src.modules.organization.router import router as router_organization
from src.modules.scene.router import router as router_scene
from src.modules.online.router import router as router_online
from src.modules.chatting.router import router as router_chatting

routers = [
    router_providers,
    router_users,
    router_files,
    router_organization,
    router_scene,
    router_online,
    router_chatting,
]

__all__ = ["routers"]
