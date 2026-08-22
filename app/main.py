from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi import HTTPException

from db import SessionLocal, get_db
from models import Product


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

class ProductCreate(BaseModel):
    name: str
    price: float = Field(gt=0)


@app.post("/products")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = Product(
        name=product.name,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "id": new_product.id,
        "name": new_product.name,
        "price": new_product.price
    }

@app.get("/products/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "id": product.id,
        "name": product.name,
        "price": product.price
    }


class ProductUpdate(BaseModel):
    name: str
    price: float

@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = product_data.name
    product.price = product_data.price

    db.commit()
    db.refresh(product)

    return {
        "id": product.id,
        "name": product.name,
        "price": product.price
    }


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }
