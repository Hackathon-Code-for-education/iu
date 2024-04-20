from src.modules.providers.router import router as router_providers
from src.modules.user.router import router as router_users
from src.modules.files.router import router as router_files
from src.modules.organization.router import router as router_organization
from src.modules.scene.router import router as router_scene

routers = [router_providers, router_users, router_files, router_organization, router_scene]

__all__ = ["routers"]
