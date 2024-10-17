from fastapi import APIRouter, Depends, Form, HTTPException
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import session_factory
import src.schemas as schemas
from .dependencies import (create_func, 
                           create_func_without_entity_name, 
                           update_func, delete_func)
from .crud import (BrigadesOperations, LaboratoriesOperations, PersonalLaboratoriesOperations,
    PersonalWorkersOperations, ProductOperations, ProductCategoryOperations,
    PersonalCategoryOperations, EngineerPersonalOperations, ToolsOperations,
    WorksWithProductOperations, WorkshopsOperations)


product_router = APIRouter(
    prefix='/products',
    tags=['Products']
)

product_category_router = APIRouter(
    prefix="/product_categories",
    tags=['Product category']
)

personal_category_router = APIRouter(
    prefix='/personal_categories',
    tags=['Personal category']
)

engineer_personal_router = APIRouter(
    prefix='/engineer_personal',
    tags=['Engineer personal']
)

personal_workers_router = APIRouter(
    prefix='/personal_workers',
    tags=['Personal workers']
)

brigades_router = APIRouter(
    prefix='/brigades',
    tags=['Brigades']
)

workshops_router = APIRouter(
    prefix='/workshops',
    tags=['Workshops']
)

laboratories_router = APIRouter(
    prefix='/laboratories',
    tags=['Laboratories']
)

personal_laboratories_router = APIRouter(
    prefix='/personal_laboratories',
    tags=['Personal laboratories']
)

tools_router = APIRouter(
    prefix='/tools',
    tags=['Tools']
)

works_with_product_router = APIRouter(
    prefix='/works_with_product',
    tags=['Works with product']
)

async def get_db():
    async with session_factory() as db:
        try:
            yield db
        finally:
            await db.close()

class ProductRouter:
    @product_router.get('/', response_model=list[schemas.Product])
    async def read_products(db: AsyncSession = Depends(get_db)):
        return await ProductOperations.get_products(db)

    @product_router.post('/', response_model=schemas.Product)
    async def create_product(product: Annotated[schemas.CreateProduct, Form()], db: AsyncSession = Depends(get_db)):
        return await create_func(ProductOperations.get_products,
                                                      ProductOperations.create_product, 
                                                      db, 
                                                      product,
                                                      'Продукт')

    @product_router.get('/{product_name}', response_model=schemas.Product)
    async def get_product(product_name: str, db: AsyncSession = Depends(get_db)):
        db_product = await ProductOperations.get_product(db, product_name)
        if db_product is None:
            raise HTTPException(status_code=400, detail='Продукт с таким именем не существует')

        return db_product

    @product_router.patch('/{product_name}', response_model=dict)
    async def update_product(product: Annotated[schemas.UpdateProduct, Form()], db: AsyncSession = Depends(get_db)):
        return await update_func(get_func=ProductOperations.get_products,
                                 update_func=ProductOperations.update_product,
                                 db=db, 
                                 something=product,
                                 entity_name='Продукт')

    @product_router.delete('/{product_id}', response_model=dict)
    async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
        return await delete_func(get_func=ProductOperations.get_products,
                                 del_func=ProductOperations.delete_product,
                                 db=db, 
                                 something_id=product_id,
                                 entity_name='Продукт')

class ProductCategoryRouter:
    @product_category_router.get('/', response_model=list[schemas.ProductCategory])
    async def get_product_categories(db: AsyncSession = Depends(get_db)):
        categories = await ProductCategoryOperations.get_product_categories(db)
        return categories

    @product_category_router.post('/', response_model=schemas.ProductCategory)
    async def create_product_category(product_category: Annotated[schemas.CreateProductCategory, Form()], 
                                      db: AsyncSession = Depends(get_db)):
        return await create_func(get_func=ProductCategoryOperations.get_product_categories,
                                                     create_func=ProductCategoryOperations.create_product_category, 
                                                     db=db, 
                                                     something=product_category,
                                                     entity_name='Категория')

    # PATCH для обновления категории продукта
    @product_category_router.patch('/{category_id}', response_model=dict)
    async def update_product_category(category: Annotated[schemas.ProductCategory, Form()], db: AsyncSession = Depends(get_db)):
        return await update_func(get_func=ProductCategoryOperations.get_product_categories,
                                 update_func=ProductCategoryOperations.update_product_category,
                                 db=db, 
                                 something=category,
                                 entity_name='Категория продукта')

    # DELETE для удаления категории продукта
    @product_category_router.delete('/{category_id}', response_model=dict)
    async def delete_product_category(category_id: int, db: AsyncSession = Depends(get_db)):
        return await delete_func(get_func=ProductOperations.get_products,
                                 update_func=ProductOperations.delete_product,
                                 db=db, 
                                 something_id=category_id,
                                 entity_name='Категория продукта')

class PersonCategoryRouter:
    @personal_category_router.get('/', response_model=list[schemas.PersonalCategory])
    async def get_personal_categories(db: AsyncSession = Depends(get_db)):
        return await PersonalCategoryOperations.get_personal_categories(db)

    @personal_category_router.post('/', response_model=schemas.PersonalCategory)
    async def create_personal_category(personal_category: Annotated[schemas.CreatePersonalCategory, Form()], db: AsyncSession = Depends(get_db)):
        return await create_func(get_func=PersonalCategoryOperations.get_personal_categories,
                                                     create_func=PersonalCategoryOperations.create_personal_category, 
                                                     db=db, 
                                                     something=personal_category,
                                                     entity_name='Категория персонала')

    # PATCH для обновления категории персонала
    @personal_category_router.patch('/{category_id}', response_model=dict)
    async def update_personal_category(category: Annotated[schemas.PersonalCategory, Form()], db: AsyncSession = Depends(get_db)):
        return await update_func(get_func=PersonalCategoryOperations.get_personal_categories,
                                 update_func=PersonalCategoryOperations.update_personal_category,
                                 db=db, 
                                 something=category,
                                 entity_name='Категория персонала')

    # DELETE для удаления категории персонала
    @personal_category_router.delete('/{category_id}', response_model=dict)
    async def delete_personal_category(category_id: int, db: AsyncSession = Depends(get_db)):
        return await delete_func(get_func=PersonalCategoryOperations.get_personal_categories,
                                 update_func=PersonalCategoryOperations.delete_personal_category,
                                 db=db, 
                                 something_id=category_id,
                                 entity_name='Категория продукта')

class EngineerPersonalRouter:
    @engineer_personal_router.get('/', response_model=list[schemas.EngineerPersonal])
    async def get_engineer_personal(db: AsyncSession = Depends(get_db)):
        return await EngineerPersonalOperations.get_engineer_personal(db)

    @engineer_personal_router.post('/', response_model=schemas.EngineerPersonal)
    async def create_engineer_person(person: Annotated[schemas.CreateEngineerPersonal, Form()], db: AsyncSession = Depends(get_db)):
        return await create_func_without_entity_name(create_func=EngineerPersonalOperations.create_engineer_personal,
                                          db=db,
                                          something=person)

    @engineer_personal_router.get('/{person_id}', response_model=schemas.EngineerPersonal)
    async def get_engineer_person(person_id: int, db: AsyncSession = Depends(get_db)):
        db_person = await EngineerPersonalOperations.get_engineer_person(db, person_id)
        if db_person is None:
            raise HTTPException(status_code=400, detail='Такого работника не существует')

        return db_person

    # PATCH для обновления инженера
    @engineer_personal_router.patch('/{person_id}', response_model=dict)
    async def update_engineer_person(person: Annotated[schemas.UpdateEngineerPersonal, Form()], db: AsyncSession = Depends(get_db)):
        return await update_func(get_func=EngineerPersonalOperations.get_engineer_personal,
                                 update_func=EngineerPersonalOperations.update_engineer_personal,
                                 db=db, 
                                 something=person,
                                 entity_name='Инженер')

    # DELETE для удаления инженера
    @engineer_personal_router.delete('/{person_id}', response_model=dict)
    async def delete_engineer_person(person_id: int, db: AsyncSession = Depends(get_db)):
        return await delete_func(get_func=EngineerPersonalOperations.get_engineer_personal,
                                 update_func=EngineerPersonalOperations.delete_engineer_personal,
                                 db=db, 
                                 something_id=person_id,
                                 entity_name='Инженер')

class PersonalWorkersRouter:
    @personal_workers_router.get('/', response_model=list[schemas.PersonalWorkers])
    async def get_personal_workers(db: AsyncSession = Depends(get_db)):
        return await PersonalWorkersOperations.get_personal_workers(db)

    @personal_workers_router.post('/', response_model=schemas.PersonalWorkers)
    async def create_personal_worker(worker: Annotated[schemas.CreatePersonalWorkers, Form()], db: AsyncSession = Depends(get_db)):
        return await create_func_without_entity_name(create_func=PersonalWorkersOperations.create_personal_worker,
                                          db=db,
                                          something=worker)

    @personal_workers_router.get('/{person_id}', response_model=schemas.PersonalWorkers)
    async def get_personal_worker(worker_id: int, db: AsyncSession = Depends(get_db)):
        db_worker = await PersonalWorkersOperations.get_personal_worker(db, worker_id)
        if db_worker is None:
            raise HTTPException(status_code=400, detail='Работника с таким именем не существует')

        return db_worker

    # PATCH для обновления персонала лаборатории
    @personal_workers_router.patch('/{person_id}', response_model=dict)
    async def update_personal_workers(person: Annotated[schemas.UpdatePersonalWorkers, Form()], db: AsyncSession = Depends(get_db)):
        return await update_func(get_func=PersonalWorkersOperations.get_personal_workers,
                                 update_func=PersonalWorkersOperations.update_personal_worker,
                                 db=db, 
                                 something=person,
                                 entity_name='Работник')

    # DELETE для удаления персонала лаборатории
    @personal_workers_router.delete('/{person_id}', response_model=dict)
    async def delete_personal_workers(person_id: int, db: AsyncSession = Depends(get_db)):
        return await delete_func(get_func=PersonalWorkersOperations.get_personal_workers,
                                 update_func=PersonalWorkersOperations.delete_personal_worker,
                                 db=db, 
                                 something_id=person_id,
                                 entity_name='Работник')

class BrigadesRouter:
    @brigades_router.get('/', response_model=list[schemas.Brigades])
    async def get_brigades(db: AsyncSession = Depends(get_db)):
        return await BrigadesOperations.get_brigades(db)

    @brigades_router.post('/', response_model=schemas.Brigades)
    async def create_brigade(brigade: Annotated[schemas.CreateBrigades, Form()], db: AsyncSession = Depends(get_db)):
        return await create_func(get_func=BrigadesOperations.get_brigades,
                                 create_func=BrigadesOperations.create_brigade,
                                 db=db,
                                 something=brigade,
                                 entity_name='Бригада')

    @brigades_router.get('/{brigade_id}', response_model=schemas.Brigades)
    async def get_brigade(brigade_id: int, db: AsyncSession = Depends(get_db)):
        try:
            db_brigade = await BrigadesOperations.get_brigade(db, brigade_id)
        except:
            raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

        if not db_brigade:
            raise HTTPException(status_code=400, detail='Бригады с таким именем не существует')

        return db_brigade

    # PATCH для обновления бригады
    @brigades_router.patch('/{brigade_id}', response_model=dict)
    async def update_brigade(brigade: Annotated[schemas.UpdateBrigades, Form()], db: AsyncSession = Depends(get_db)):
        return await update_func(get_func=BrigadesOperations.get_brigades,
                                 update_func=BrigadesOperations.update_brigade,
                                 db=db, 
                                 something=brigade,
                                 entity_name='Бригада')

    # DELETE для удаления бригады
    @brigades_router.delete('/{brigade_id}', response_model=dict)
    async def delete_brigade(brigade_id: int, db: AsyncSession = Depends(get_db)):
        return await delete_func(get_func=BrigadesOperations.get_brigades,
                                 update_func=BrigadesOperations.delete_brigade,
                                 db=db, 
                                 something_id=brigade_id,
                                 entity_name='Бригада')

class WorkshopsRouter:
    @workshops_router.get('/', response_model=list[schemas.Workshop])
    async def get_workshops(db: AsyncSession = Depends(get_db)):
        return await WorkshopsOperations.get_workshops(db)

    @workshops_router.post('/', response_model=schemas.Workshop)
    async def create_workshop(workshop: Annotated[schemas.CreateWorkshop, Form()], db: AsyncSession = Depends(get_db)):
        return await create_func(get_func=WorkshopsOperations.get_workshops,
                                 create_func=WorkshopsOperations.create_workshop,
                                 db=db,
                                 something=workshop,
                                 entity_name='Цех')

    # PATCH для обновления цеха
    @workshops_router.patch('/{workshop_id}', response_model=dict)
    async def update_workshop(workshop: Annotated[schemas.UpdateWorkshop, Form()], db: AsyncSession = Depends(get_db)):
        return await update_func(get_func=WorkshopsOperations.get_workshops,
                                 update_func=WorkshopsOperations.update_workshop,
                                 db=db, 
                                 something=workshop,
                                 entity_name='Цех')

    # DELETE для удаления цеха
    @workshops_router.delete('/{workshop_id}', response_model=dict)
    async def delete_workshop(workshop_id: int, db: AsyncSession = Depends(get_db)):
        return await delete_func(get_func=WorkshopsOperations.get_workshops,
                                 update_func=WorkshopsOperations.delete_workshop,
                                 db=db, 
                                 something_id=workshop_id,
                                 entity_name='Цех')

class LaboratoriesRouter:
    @laboratories_router.get('/', response_model=list[schemas.TestLaboratories])
    async def get_laboratories(db: AsyncSession = Depends(get_db)):
        return await LaboratoriesOperations.get_laboratories(db)

    @laboratories_router.post('/', response_model=schemas.TestLaboratories)
    async def create_laboratory(laboratory: Annotated[schemas.CreateLaboratory, Form()], db: AsyncSession = Depends(get_db)):
        return await create_func(get_func=LaboratoriesOperations.get_laboratories,
                                 create_func=LaboratoriesOperations.create_laboratory,
                                 db=db,
                                 something=laboratory,
                                 entity_name='Лаборатория')

    @laboratories_router.get('/{laboratory_name}', response_model=schemas.TestLaboratories)
    async def get_laboratory(laboratory_name: str, db: AsyncSession = Depends(get_db)):
        laboratory = await LaboratoriesOperations.get_laboratory(db, laboratory_name)
        if laboratory is None:
            raise HTTPException(status_code=400, detail='Название лаборатории введено неверно')
        return laboratory

    # PATCH для обновления лаборатории
    @laboratories_router.patch('/{laboratory_id}', response_model=dict)
    async def update_laboratory(laboratory: Annotated[schemas.TestLaboratories, Form()], db: AsyncSession = Depends(get_db)):
        return await update_func(get_func=LaboratoriesOperations.get_laboratories,
                                 update_func=LaboratoriesOperations.update_laboratory,
                                 db=db, 
                                 something=laboratory,
                                 entity_name='Лаборатория')

    # DELETE для удаления лаборатории
    @laboratories_router.delete('/{laboratory_id}', response_model=dict)
    async def delete_laboratory(laboratory_id: int, db: AsyncSession = Depends(get_db)):
       return await delete_func(get_func=LaboratoriesOperations.get_laboratories,
                                 update_func=LaboratoriesOperations.delete_laboratory,
                                 db=db, 
                                 something_id=laboratory_id,
                                 entity_name='Лаборатория')

class PersonalLaboratoriesRouter:
    @personal_laboratories_router.get('/', response_model=list[schemas.PersonalLaboratories])
    async def get_personal_laboratories(db: AsyncSession = Depends(get_db)):
        return await PersonalLaboratoriesOperations.get_personal_laboratories(db)

    @personal_laboratories_router.post('/', response_model=schemas.PersonalLaboratories)
    async def create_person_laboratory(person: Annotated[schemas.CreatePersonalLaboratory, Form()], db: AsyncSession = Depends(get_db)):
        return await create_func_without_entity_name(create_func=PersonalLaboratoriesOperations.create_person_laboratory,
                                          db=db,
                                          something=person)

    @personal_laboratories_router.get('/{person_id}', response_model=schemas.PersonalLaboratories)
    async def get_person_laboratory(person_id: int, db: AsyncSession = Depends(get_db)):
        db_person = await PersonalLaboratoriesOperations.get_person_laboratory(db, person_id)
        if not db_person:
            raise HTTPException(status_code=400, detail='Работника с таким id не существует')

        return db_person

    # PATCH для обновления персонала лаборатории
    @personal_laboratories_router.patch('/{person_id}', response_model=dict)
    async def update_personal_laboratory(person: Annotated[schemas.UpdatePersonalLaboratory, Form()], db: AsyncSession = Depends(get_db)):
        return await update_func(get_func=PersonalLaboratoriesOperations.get_personal_laboratories,
                                 update_func=PersonalLaboratoriesOperations.update_personal_laboratory,
                                 db=db, 
                                 something=person,
                                 entity_name='Работник')

    # DELETE для удаления персонала лаборатории
    @personal_laboratories_router.delete('/{person_id}', response_model=dict)
    async def delete_personal_laboratory(person_id: int, db: AsyncSession = Depends(get_db)):
        return await delete_func(get_func=PersonalLaboratoriesOperations.get_personal_laboratories,
                                 update_func=PersonalLaboratoriesOperations.delete_personal_laboratory,
                                 db=db, 
                                 something_id=person_id,
                                 entity_name='Работник')

class ToolsRouter:
    @tools_router.get('/', response_model=list[schemas.Tools])
    async def get_tools(db: AsyncSession = Depends(get_db)):
        return await ToolsOperations.get_tools(db)

    @tools_router.post('/', response_model=schemas.Tools)
    async def create_tool(tool: Annotated[schemas.CreateTool, Form()], db: AsyncSession = Depends(get_db)):
        return await create_func_without_entity_name(create_func=ToolsOperations.create_tools,
                                                     db=db,
                                                     something=tool)

    # PATCH для обновления инструмента
    @tools_router.patch('/{tool_id}', response_model=dict)
    async def update_tool(tool: Annotated[schemas.UpdateTool, Form()], db: AsyncSession = Depends(get_db)):
        return await update_func(get_func=ToolsOperations.get_tools,
                                 update_func=ToolsOperations.update_tool,
                                 db=db, 
                                 something=tool,
                                 entity_name='Инструмент')

    # DELETE для удаления инструмента
    @tools_router.delete('/{tool_id}', response_model=dict)
    async def delete_tool(tool_id: int, db: AsyncSession = Depends(get_db)):
        return await delete_func(get_func=ToolsOperations.get_tools,
                                 update_func=ToolsOperations.delete_tool,
                                 db=db, 
                                 something_id=tool_id,
                                 entity_name='Инструмент')

class WorksWithProductRouter:
    @works_with_product_router.get('/', response_model=list[schemas.WorksWithProduct])
    async def get_works_for_product(db: AsyncSession = Depends(get_db)):
        return await WorksWithProductOperations.get_works_with_product(db)

    @works_with_product_router.post('/', response_model=schemas.WorksWithProduct)
    async def create_work_for_product(work: Annotated[schemas.CreateWorkForProduct, Form()], db: AsyncSession = Depends(get_db)):
        return await create_func(get_func=WorksWithProductOperations.get_works_with_product,
                                 create_func=WorksWithProductOperations.create_work_for_product,
                                 db=db,
                                 something=work,
                                 entity_name='Работа для продукта')

    # PATCH для обновления работы с продуктом
    @works_with_product_router.patch('/{work_id}', response_model=dict)
    async def update_work_with_product(work: Annotated[schemas.UpdateWorkForProduct, Form()], db: AsyncSession = Depends(get_db)):
        return await update_func(get_func=WorksWithProductOperations.get_works_with_product,
                                 update_func=WorksWithProductOperations.update_work_with_product,
                                 db=db, 
                                 something=work,
                                 entity_name='Работа с продуктом')

    # DELETE для удаления работы с продуктом
    @works_with_product_router.delete('/{work_id}', response_model=dict)
    async def delete_work_with_product(work_id: int, db: AsyncSession = Depends(get_db)):
        return await delete_func(get_func=WorksWithProductOperations.get_works_with_product,
                                 update_func=WorksWithProductOperations.delete_work_with_product,
                                 db=db, 
                                 something_id=work_id,
                                 entity_name='Работа с продуктом')
