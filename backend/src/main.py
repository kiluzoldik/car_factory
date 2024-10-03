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

# готово
@app.get('/products', response_model=list[schemas.Product])
async def read_products(db: AsyncSession = Depends(get_db)):
    products = await crud.get_products(db)
    return products

# готово
@app.post('/product', response_model=schemas.Product)
async def create_product(product: schemas.CreateProduct, db: AsyncSession = Depends(get_db)):
    check_product = await crud.get_product(db, product.name)
    if check_product:
        raise HTTPException(status_code=400, detail='Продукт уже существует')

    try:
        db_product = await crud.create_product(db, product)
    except:
        raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

    return db_product

# готово
@app.get('/products/{product_name}', response_model=schemas.Product)
async def get_product(db: AsyncSession = Depends(get_db), product_name: str | None = None):
    db_product = await crud.get_product(db, product_name)
    if db_product is None:
        raise HTTPException(status_code=400, detail='Продукт с таким именем не существует')

    return db_product

# готово
@app.get('/product_categories', response_model=list[schemas.ProductCategory])
async def get_product_categories(db: AsyncSession = Depends(get_db)):
    categories = await crud.get_product_categories(db)
    return categories

# готово
@app.post('/product_category', response_model=schemas.ProductCategory)
async def create_product_category(product_category: schemas.CreateProductCategory, db: AsyncSession = Depends(get_db)):
    check_category = await crud.get_product_categories(db)
    if product_category.name in [category.name for category in check_category]:
        raise HTTPException(status_code=400, detail='Категория существует')

    try:
        db_categories = await crud.create_product_category(db, product_category)
    except:
        raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

    return db_categories

# готово
@app.get('/personal_categories', response_model=list[schemas.PersonalCategory])
async def get_personal_categories(db: AsyncSession = Depends(get_db)):
    categories = await crud.get_personal_categories(db)
    if not categories:
        raise HTTPException(status_code=400, detail='Не одной категории персонала не существует')
    return categories

# готово
@app.post('/personal_category', response_model=schemas.PersonalCategory)
async def create_personal_category(personal_category: schemas.CreatePersonalCategory, db: AsyncSession = Depends(get_db)):
    check_category = await crud.get_personal_categories(db)
    if personal_category.name in [item.name for item in check_category]:
        raise HTTPException(status_code=400, detail='Категория уже существует')

    try:
        db_personal_category = await crud.create_personal_category(db, personal_category)
    except:
        raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

    return db_personal_category

# готово
@app.get('/engineer_personal', response_model=list[schemas.EngineerPersonal])
async def get_engineer_personal(db: AsyncSession = Depends(get_db)):
    personal = await crud.get_engineer_personal(db)
    if not personal:
        raise HTTPException(status_code=400, detail='Работников-инженеров не существует')
    return personal

# готово
@app.post('/engineer_person', response_model=schemas.EngineerPersonal)
async def create_engineer_person(person: schemas.CreateEngineerPersonal, db: AsyncSession = Depends(get_db)):
    try:
        db_person = await crud.create_engineer_personal(db, person)
    except:
        raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

    return db_person

# готово
@app.get('/engineer_personal/{person_id}', response_model=schemas.EngineerPersonal)
async def get_engineer_person(person_id: int, db: AsyncSession = Depends(get_db)):
    db_person = await crud.get_engineer_person(db, person_id)
    if db_person is None:
        raise HTTPException(status_code=400, detail='Такого работника не существует')

    return db_person

# готово
@app.get('/personal_workers', response_model=list[schemas.PersonalWorkers])
async def get_personal_workers(db: AsyncSession = Depends(get_db)):
    db_workers = await crud.get_personal_workers(db)
    if not db_workers:
        raise HTTPException(status_code=400, detail='Список работников не существует')

    return db_workers

# готово
@app.post('/personal_worker', response_model=schemas.PersonalWorkers)
async def create_personal_worker(worker: schemas.CreatePersonalWorkers, db: AsyncSession = Depends(get_db)):
    try:
        db_worker = await crud.create_personal_worker(db, worker)
    except:
        raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')
    return db_worker

# готово
@app.get('/personal_workers/{person_id}', response_model=schemas.PersonalWorkers)
async def get_personal_worker(worker_id: int, db: AsyncSession = Depends(get_db)):
    db_worker = await crud.get_personal_worker(db, worker_id)
    if db_worker is None:
        raise HTTPException(status_code=400, detail='Работника с таким именем не существует')

    return db_worker

# готово
@app.get('/brigades', response_model=list[schemas.Brigades])
async def get_brigades(db: AsyncSession = Depends(get_db)):
    db_brigades = await crud.get_brigades(db)
    if not db_brigades:
        raise HTTPException(status_code=400, detail='Бригад не существует')

    return db_brigades

# готово
@app.post('/brigades', response_model=schemas.Brigades)
async def create_brigade(brigade: schemas.CreateBrigades, db: AsyncSession = Depends(get_db)):
    check_brigade = await crud.get_brigades(db)
    if brigade.name in [item.name for item in check_brigade]:
        raise HTTPException(status_code=400, detail='Бригада с таким id уже существует')

    try:
        db_brigade = await crud.create_brigade(db, brigade)
    except:
        raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

    return db_brigade

# готово
@app.get('/brigades/{brigade_id}', response_model=schemas.Brigades)
async def get_brigade(brigade_id: int, db: AsyncSession = Depends(get_db)):
    try:
        db_brigade = await crud.get_brigade(db, brigade_id)
    except:
        raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

    if not db_brigade:
        raise HTTPException(status_code=400, detail='Бригады с таким именем не существует')

    return db_brigade

# готово
@app.get('/workshops', response_model=list[schemas.Workshop])
async def get_workshops(db: AsyncSession = Depends(get_db)):
    db_workshops = await crud.get_workshops(db)
    if not db_workshops:
        raise HTTPException(status_code=400, detail='Список цехов пуст')

    return db_workshops

# готово
@app.post('/workshop', response_model=schemas.Workshop)
async def create_workshop(workshop: schemas.CreateWorkshop, db: AsyncSession = Depends(get_db)):
    check_workshop = await crud.get_workshops(db)
    if workshop.name in [item.name for item in check_workshop]:
        raise HTTPException(status_code=400, detail='Цех с таким названием уже существует')

    try:
        db_workshop = await crud.create_workshop(db, workshop)
    except:
        raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

    return db_workshop

# готово
@app.get('/laboratories', response_model=list[schemas.TestLaboratories])
async def get_laboratories(db: AsyncSession = Depends(get_db)):
    db_laboratories = await crud.get_laboratories(db)
    return db_laboratories

# готово
@app.post('/laboratories', response_model=schemas.TestLaboratories)
async def create_laboratory(laboratory: schemas.CreateLaboratory, db: AsyncSession = Depends(get_db)):
    check_laboratory = await crud.get_laboratories(db)
    if laboratory.name in [item.name for item in check_laboratory]:
        raise HTTPException(status_code=400, detail='Лаборатория уже существует')

    try:
        db_laboratory = await crud.create_laboratory(db, laboratory)
    except:
        raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

    return db_laboratory

# готово
@app.get('/laboratories/{laboratory_name}', response_model=schemas.TestLaboratories)
async def get_laboratory(db: AsyncSession = Depends(get_db), laboratory_name: str | None = None):
    laboratory = await crud.get_laboratory(db, laboratory_name)
    if laboratory is None:
        raise HTTPException(status_code=400, detail='Название лаборатории введено неверно')
    return laboratory

# готово
@app.get('/personal_laboratories', response_model=list[schemas.PersonalLaboratories])
async def get_personal_laboratories(db: AsyncSession = Depends(get_db)):
    db_personal = await crud.get_personal_laboratories(db)
    if not db_personal:
        raise HTTPException(status_code=400, detail='Работников для лабораторий не существует')

    return db_personal

# готово
@app.post('/person_laboratory', response_model=schemas.PersonalLaboratories)
async def create_person_laboratory(person: schemas.CreatePersonalLaboratory, db: AsyncSession = Depends(get_db)):
    try:
        db_person = await crud.create_person_laboratory(db, person)
    except:
        raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

    return db_person

# готово
@app.get('/personal_laboratories/{person_id}', response_model=schemas.PersonalLaboratories)
async def get_person_laboratory(person_id: int, db: AsyncSession = Depends(get_db)):
    db_person = await crud.get_person_laboratory(db, person_id)
    if not db_person:
        raise HTTPException(status_code=400, detail='Работника с таким id не существует')

    return db_person

# готово
@app.get('/tools', response_model=list[schemas.Tools])
async def get_tools(db: AsyncSession = Depends(get_db)):
    tools = await crud.get_tools(db)
    if not tools:
        raise HTTPException(status_code=400, detail='Инструментов не существует')

    return tools

# готово
@app.post('/tool', response_model=schemas.Tools)
async def create_tool(tool: schemas.CreateTool, db: AsyncSession = Depends(get_db)):
    try:
        db_tool = await crud.create_tools(db, tool)
    except:
        raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

    return db_tool

# готово
@app.get('/works_with_product', response_model=list[schemas.WorksWithProduct])
async def get_works_for_product(db: AsyncSession = Depends(get_db)):
    db_works = await crud.get_works_with_product(db)
    if not db_works:
        raise HTTPException(status_code=400, detail='Работ для продуктов не существует')

    return db_works

# готово
@app.post('/work_with_product', response_model=schemas.WorksWithProduct)
async def create_work_for_product(work: schemas.CreateWorkForProduct, db: AsyncSession = Depends(get_db)):
    check_work = await crud.get_works_with_product(db)
    if work.name in [item.name for item in check_work]:
        raise HTTPException(status_code=400, detail='Работа для продукта с таким названием уже существует')

    try:
        db_work = await crud.create_work_for_product(db, work)
    except:
        raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

    return db_work