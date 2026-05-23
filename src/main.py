from fastapi import FastAPI
from src.api import products
from src.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "B2B Service"}