import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Tatkal Multi Website Key System")

@app.get("/")
def home():
    return {
        "status": "online",
        "system": "Tatkal Key System"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/products")
def products():
    return {
        "products": [],
        "message": "Product database will be connected next"
    }

@app.get("/licences")
def licences():
    return {
        "licences": [],
        "message": "Licence database will be connected next"
    }
  
