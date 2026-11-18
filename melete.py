##########
# IMPORT #
##########
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from src.backend.endpoints import consequences, variants

########
# MAIN #
########
app = FastAPI()

# First middleware is the last to be applied to incomming request, and first to response.
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(variants.router)
app.include_router(consequences.router)
