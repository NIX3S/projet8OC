from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.exceptions import validation_exception_handler
from app.api.endpoints import router

app = FastAPI(title="Prêt à Dépenser - Scoring API", version="1.0.0")

# Enregistrer le handler avant les routes
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Un seul router
app.include_router(router)
