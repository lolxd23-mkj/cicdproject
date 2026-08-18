from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session

from db import Base, engine, SessionLocal, get_db
from models import Product


Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevOps E-commerce API")


@app.get("/")
def root():
    return {"message": "E-commerce API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    return [
         {
             "id": product.id,
             "name": product.name,
             "price": product.price,
         }
         for product in products
    ]


@app.get("/version")
def version():
    return {"version": "1.0.0"}
