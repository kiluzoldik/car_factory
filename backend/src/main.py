from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import session_factory
import src.schemas as schemas
import src.crud as crud


app = FastAPI()

async def get_db():
    async with session_factory() as db:
        try:
            yield db
        finally:
            await db.close()

@app.get('/products', response_model=list[schemas.Product])
async def read_products(db: AsyncSession = Depends(get_db)):
    product = await crud.get_products(db)
    return product

@app.post('/products', response_model=schemas.Product)
async def create_product(product: schemas.CreateProduct, db: AsyncSession = Depends(get_db)):
    check_product = await crud.get_product(db, product.id)
    if check_product:
        raise HTTPException(status_code=400, detail='Product is already created')

    db_product = await crud.create_product(db, product)
    return db_product

@app.get('/products/{product_id}')
def home_page():
    return 'hello'

@app.get('/product_categories', response_model=schemas.ProductCategory)
async def get_product_categories(db: AsyncSession = Depends(get_db)):
    categories = await crud.get_product_categories(db)
    return categories

@app.post('/product_categories', response_model=schemas.ProductCategory)
async def create_product_category(product_category: schemas.CreateProductCategory, db: AsyncSession = Depends(get_db)):
    check_category = await crud.get_product_categories(db)
    if product_category.name in [category.name for category in check_category]:
        raise HTTPException(status_code=400, detail='Category already created')

    return await crud.create_product_category(db, product_category)

@app.get('/personal_categories')
async def get_personal_categories(db: AsyncSession = Depends(get_db)):
    categories = await crud.get_personal_categories(db)
    return categories

@app.post('/personal_category', response_model=schemas.PersonalCategory)
async def create_personal_category(personal_category: schemas.CreatePersonalCategory, db: AsyncSession = Depends(get_db)):
    check_category = await crud.get_personal_categories(db)
    if personal_category in check_category:
        raise HTTPException(status_code=400, detail='Категория уже существует')

    db_personal_category = await crud.create_personal_category(db, personal_category)
    return db_personal_category

# @app.get('/engineer_personal')
# def home_page():
#     return 'hello'
#
# @app.get('/engineer_personal/{person_id}')
# def home_page():
#     return 'hello'
#
# @app.get('/personal_workers')
# def home_page():
#     return 'hello'
#
# @app.get('/personal_workers/{person_id}')
# def home_page():
#     return 'hello'
#
# @app.get('/brigades')
# def home_page():
#     return 'hello'
#
# @app.get('/brigades/{brigade_id}')
# def home_page():
#     return 'hello'
#
# @app.get('/workshops')
# def home_page():
#     return 'hello'
#
# @app.get('/workshops/{workshop_id}')
# def home_page():
#     return 'hello'

@app.get('/laboratories', response_model=list[schemas.TestLaboratories])
async def get_laboratories(db: AsyncSession = Depends(get_db)):
    db_laboratories = await crud.get_laboratories(db)
    return db_laboratories

@app.post('/laboratories', response_model=schemas.TestLaboratories)
async def create_laboratory(laboratory: schemas.CreateLaboratory, db: AsyncSession = Depends(get_db)):
    check_laboratory = await crud.get_laboratory(db, laboratory.id)
    if check_laboratory:
        raise HTTPException(status_code=400, detail='Лаборатория уже существует')

    db_laboratory = await crud.create_laboratory(db, laboratory)
    return db_laboratory

@app.get('/laboratories/{laboratory_id}', response_model=schemas.TestLaboratories)
async def get_laboratory(db: AsyncSession = Depends(get_db), laboratory_id: Annotated[int, None] = None):
    laboratory = await crud.get_laboratory(db, laboratory_id)
    return laboratory

# @app.get('/personal_laboratories')
# def home_page():
#     return 'hello'
#
# @app.get('/personal_laboratories/{person_id}')
# def home_page():
#     return 'hello'
#
# @app.get('/tools')
# def home_page():
#     return 'hello'
#
# @app.get('/works_with_product')
# def home_page():
#     return 'hello'
