##########
# IMPORT #
##########
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.endpoints import consequences, variants

########
# MAIN #
########
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You should restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(variants.router)
app.include_router(consequences.router)
