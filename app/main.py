from fastapi import FastAPI

app = FastAPI(title="DevOps E-commerce API")


@app.get("/")
def root():
    return {"message": "E-commerce API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/products")
def get_products():
    return [
        {"id": 1, "name": "Laptop", "price": 1200},
        {"id": 2, "name": "Keyboard", "price": 80},
        {"id": 3, "name": "Mouse", "price": 40},
    ]

@app.get("/version")
def version():
    return {"version": "Br0ken"}
