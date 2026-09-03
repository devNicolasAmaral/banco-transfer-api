from fastapi import FastAPI

from app.routers.transfer import router as transfer_router
from app.routers.user import router as user_router


app = FastAPI(
    title="Banco Transfer API",
    version="0.1.0",
)

app.include_router(transfer_router)
app.include_router(user_router)