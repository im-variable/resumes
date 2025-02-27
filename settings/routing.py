import importlib
import pkgutil
from fastapi import APIRouter
import routers

# Import custom route mappings from routes.py
from routes import app_routes

router = APIRouter()

# Dynamically import and include all routers from 'routers' package
for _, module_name, _ in pkgutil.iter_modules(routers.__path__):
    module = importlib.import_module(f"routers.{module_name}")
    
    if hasattr(module, "router"):
        prefix = app_routes.get(module_name, f"/{module_name}")
        router.include_router(module.router, prefix=prefix, tags=[module_name.capitalize()])
