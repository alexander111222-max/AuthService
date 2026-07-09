import logging
import uvicorn
from fastapi import FastAPI

from src.api.auth import router as auth_router
from src.api.users import router as users_router
from src.api.entities import router as entities_router
from src.api.permissions import router as permissions_router
from src.api.roles import router as roles_router
from src.api.mock import router as mock_router
from src.api.seed import router as seed_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(entities_router)
app.include_router(permissions_router)
app.include_router(roles_router)
app.include_router(mock_router)
app.include_router(seed_router)


if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port=8000)