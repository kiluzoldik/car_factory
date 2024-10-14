from fastapi import APIRouter, Depends, Form, HTTPException
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import session_factory
import src.schemas as schemas
from .crud import BrigadesOperations, LaboratoriesOperations, PersonalLaboratoriesOperations, \
    PersonalWorkersOperations, ProductOperations, ProductCategoryOperations, \
    PersonalCategoryOperations, EngineerPersonalOperations, ToolsOperations, \
    WorksWithProductOperations, WorkshopsOperations


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
    # готово
    @product_router.get('/', response_model=list[schemas.Product])
    async def read_products(db: AsyncSession = Depends(get_db)):
        products = await ProductOperations.get_products(db)
        return products

    # готово
    @product_router.post('/', response_model=schemas.Product)
    async def create_product(product: Annotated[schemas.CreateProduct, Form()], db: AsyncSession = Depends(get_db)):
        check_product = await ProductOperations.get_product(db, product.name)
        if check_product:
            raise HTTPException(status_code=400, detail='Продукт уже существует')

        try:
            db_product = await ProductOperations.create_product(db, product)
        except:
            raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

        return db_product

    # готово
    @product_router.get('/{product_name}', response_model=schemas.Product)
    async def get_product(product_name: str, db: AsyncSession = Depends(get_db)):
        db_product = await ProductOperations.get_product(db, product_name)
        if db_product is None:
            raise HTTPException(status_code=400, detail='Продукт с таким именем не существует')

        return db_product

    @product_router.patch('/{product_name}', response_model=dict)
    async def update_product(product: Annotated[schemas.UpdateProduct, Form()], db: AsyncSession = Depends(get_db)):
        try:
            await ProductOperations.update_product(db, product.id, product)
        except:
            raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')
        
        return {'detail': 'Продукт успешно изменен' }

    @product_router.delete('/{product_id}')
    async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
        return await ProductOperations.delete_product(db, product_id)

class ProductCategoryRouter:
    # готово
    @product_category_router.get('/', response_model=list[schemas.ProductCategory])
    async def get_product_categories(db: AsyncSession = Depends(get_db)):
        categories = await ProductCategoryOperations.get_product_categories(db)
        return categories

    # готово
    @product_category_router.post('/', response_model=schemas.ProductCategory)
    async def create_product_category(product_category: Annotated[schemas.CreateProductCategory, Form()], db: AsyncSession = Depends(get_db)):
        check_category = await ProductCategoryOperations.get_product_categories(db)
        if product_category.name in [category.name for category in check_category]:
            raise HTTPException(status_code=400, detail='Категория существует')

        try:
            db_categories = await ProductCategoryOperations.create_product_category(db, product_category)
        except:
            raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

        return db_categories

    # PATCH для обновления категории продукта
    @product_category_router.patch('/{category_id}', response_model=dict)
    async def update_product_category(category: Annotated[schemas.ProductCategory, Form()], db: AsyncSession = Depends(get_db)):
        db_categories = await ProductCategoryOperations.get_product_categories(db)
        if category.id not in [item.id for item in db_categories]:
            raise HTTPException(status_code=404, detail="Категория не найдена")
        
        try:
            await ProductCategoryOperations.update_product_category(db, category.id, category)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")
        
        return {'detail': 'Категория успешно изменена'}

    # DELETE для удаления категории продукта
    @product_category_router.delete('/{category_id}', response_model=dict)
    async def delete_product_category(category_id: int, db: AsyncSession = Depends(get_db)):
        db_categories = await ProductCategoryOperations.get_product_categories(db)
        if category_id not in [item.id for item in db_categories]:
            raise HTTPException(status_code=404, detail="Категория не найдена")

        try:
            await ProductCategoryOperations.delete_product_category(db, category_id)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")

        return {"detail": "Категория успешно удалена"}

class PersonCategoryRouter:
    # готово
    @personal_category_router.get('/', response_model=list[schemas.PersonalCategory])
    async def get_personal_categories(db: AsyncSession = Depends(get_db)):
        categories = await PersonalCategoryOperations.get_personal_categories(db)
        if not categories:
            raise HTTPException(status_code=400, detail='Не одной категории персонала не существует')
        return categories

    # готово
    @personal_category_router.post('/', response_model=schemas.PersonalCategory)
    async def create_personal_category(personal_category: Annotated[schemas.CreatePersonalCategory, Form()], db: AsyncSession = Depends(get_db)):
        check_category = await PersonalCategoryOperations.get_personal_categories(db)
        if personal_category.name in [item.name for item in check_category]:
            raise HTTPException(status_code=400, detail='Категория уже существует')

        try:
            db_personal_category = await PersonalCategoryOperations.create_personal_category(db, personal_category)
        except:
            raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

        return db_personal_category

    # PATCH для обновления категории персонала
    @personal_category_router.patch('/{category_id}', response_model=dict)
    async def update_personal_category(category: Annotated[schemas.PersonalCategory, Form()], db: AsyncSession = Depends(get_db)):
        db_categories = await PersonalCategoryOperations.get_personal_categories(db)
        if category.id not in [item.id for item in db_categories]:
            raise HTTPException(status_code=404, detail="Категория персонала не найдена")
        
        try:
            await PersonalCategoryOperations.update_personal_category(db, category.id, category)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")
        
        return {'detail': "Категория персонала успешно изменена"}

    # DELETE для удаления категории персонала
    @personal_category_router.delete('/{category_id}', response_model=dict)
    async def delete_personal_category(category_id: int, db: AsyncSession = Depends(get_db)):
        db_categories = await PersonalCategoryOperations.get_personal_categories(db)
        if category_id not in [item.id for item in db_categories]:
            raise HTTPException(status_code=404, detail="Категория персонала не найдена")

        try:
            await PersonalCategoryOperations.delete_personal_category(db, category_id)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")

        return {"detail": "Категория персонала успешно удалена"}

class EngineerPersonalRouter:
    # готово
    @engineer_personal_router.get('/', response_model=list[schemas.EngineerPersonal])
    async def get_engineer_personal(db: AsyncSession = Depends(get_db)):
        personal = await EngineerPersonalOperations.get_engineer_personal(db)
        if not personal:
            raise HTTPException(status_code=400, detail='Работников-инженеров не существует')
        return personal

    # готово
    @engineer_personal_router.post('/', response_model=schemas.EngineerPersonal)
    async def create_engineer_person(person: Annotated[schemas.CreateEngineerPersonal, Form()], db: AsyncSession = Depends(get_db)):
        try:
            db_person = await EngineerPersonalOperations.create_engineer_personal(db, person)
        except:
            raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

        return db_person

    # готово
    @engineer_personal_router.get('/{person_id}', response_model=schemas.EngineerPersonal)
    async def get_engineer_person(person_id: int, db: AsyncSession = Depends(get_db)):
        db_person = await EngineerPersonalOperations.get_engineer_person(db, person_id)
        if db_person is None:
            raise HTTPException(status_code=400, detail='Такого работника не существует')

        return db_person

    # PATCH для обновления инженера
    @engineer_personal_router.patch('/{person_id}', response_model=dict)
    async def update_engineer_person(person: Annotated[schemas.UpdateEngineerPersonal, Form()], db: AsyncSession = Depends(get_db)):
        db_person = await EngineerPersonalOperations.get_engineer_person(db, person.id)
        if db_person is None:
            raise HTTPException(status_code=404, detail="Инженер не найден")
        
        try:
            await EngineerPersonalOperations.update_engineer_person(db, person.id, person)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")
        
        return {'detail': 'Инженер успешно изменен'}

    # DELETE для удаления инженера
    @engineer_personal_router.delete('/{person_id}', response_model=dict)
    async def delete_engineer_person(person_id: int, db: AsyncSession = Depends(get_db)):
        db_person = await EngineerPersonalOperations.get_engineer_person(db, person_id)
        if db_person is None:
            raise HTTPException(status_code=404, detail="Инженер не найден")

        try:
            await EngineerPersonalOperations.delete_engineer_person(db, person_id)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")

        return {"detail": "Инженер успешно удален"}

class PersonalWorkersRouter:
    # готово
    @personal_workers_router.get('/', response_model=list[schemas.PersonalWorkers])
    async def get_personal_workers(db: AsyncSession = Depends(get_db)):
        db_workers = await PersonalWorkersOperations.get_personal_workers(db)
        if not db_workers:
            raise HTTPException(status_code=400, detail='Список работников не существует')

        return db_workers

    # готово
    @personal_workers_router.post('/', response_model=schemas.PersonalWorkers)
    async def create_personal_worker(worker: Annotated[schemas.CreatePersonalWorkers, Form()], db: AsyncSession = Depends(get_db)):
        try:
            db_worker = await PersonalWorkersOperations.create_personal_worker(db, worker)
        except:
            raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')
        return db_worker

    # готово
    @personal_workers_router.get('/{person_id}', response_model=schemas.PersonalWorkers)
    async def get_personal_worker(worker_id: int, db: AsyncSession = Depends(get_db)):
        db_worker = await PersonalWorkersOperations.get_personal_worker(db, worker_id)
        if db_worker is None:
            raise HTTPException(status_code=400, detail='Работника с таким именем не существует')

        return db_worker

    # PATCH для обновления персонала лаборатории
    @personal_workers_router.patch('/{person_id}', response_model=dict)
    async def update_personal_workers(person: Annotated[schemas.UpdatePersonalWorkers, Form()], db: AsyncSession = Depends(get_db)):
        db_person = await PersonalWorkersOperations.get_personal_worker(db, person.id)
        if db_person is None:
            raise HTTPException(status_code=404, detail="Работник не найден")
        
        try:
            await PersonalWorkersOperations.update_personal_worker(db, person.id, person)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")
        
        return {'detail': 'Работник успешно изменен'}

    # DELETE для удаления персонала лаборатории
    @personal_workers_router.delete('/{person_id}', response_model=dict)
    async def delete_personal_workers(person_id: int, db: AsyncSession = Depends(get_db)):
        db_person = await PersonalWorkersOperations.get_personal_worker(db, person_id)
        if db_person is None:
            raise HTTPException(status_code=404, detail="Работник не найден")

        try:
            await PersonalWorkersOperations.delete_personal_worker(db, person_id)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")

        return {"detail": "Работник успешно удален"}

class BrigadesRouter:
    # готово
    @brigades_router.get('/', response_model=list[schemas.Brigades])
    async def get_brigades(db: AsyncSession = Depends(get_db)):
        db_brigades = await BrigadesOperations.get_brigades(db)
        if not db_brigades:
            raise HTTPException(status_code=400, detail='Бригад не существует')

        return db_brigades

    # готово
    @brigades_router.post('/', response_model=schemas.Brigades)
    async def create_brigade(brigade: Annotated[schemas.CreateBrigades, Form()], db: AsyncSession = Depends(get_db)):
        check_brigade = await BrigadesOperations.get_brigades(db)
        if brigade.name in [item.name for item in check_brigade]:
            raise HTTPException(status_code=400, detail='Бригада с таким id уже существует')

        try:
            db_brigade = await BrigadesOperations.create_brigade(db, brigade)
        except:
            raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

        return db_brigade

    # готово
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
        db_brigade = await BrigadesOperations.get_brigade(db, brigade.id)
        if db_brigade is None:
            raise HTTPException(status_code=404, detail="Бригада не найдена")
        
        try:
            await BrigadesOperations.update_brigade(db, brigade.id, brigade)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")
        
        return {'detail': 'Бригада успешно изменена'}

    # DELETE для удаления бригады
    @brigades_router.delete('/{brigade_id}', response_model=dict)
    async def delete_brigade(brigade_id: int, db: AsyncSession = Depends(get_db)):
        db_brigade = await BrigadesOperations.get_brigade(db, brigade_id)
        if db_brigade is None:
            raise HTTPException(status_code=404, detail="Бригада не найдена")

        try:
            await BrigadesOperations.delete_brigade(db, brigade_id)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")

        return {"detail": "Бригада успешно удалена"}

class WorkshopsRouter:
    # готово
    @workshops_router.get('/', response_model=list[schemas.Workshop])
    async def get_workshops(db: AsyncSession = Depends(get_db)):
        db_workshops = await WorkshopsOperations.get_workshops(db)
        if not db_workshops:
            raise HTTPException(status_code=400, detail='Список цехов пуст')

        return db_workshops

    # готово
    @workshops_router.post('/', response_model=schemas.Workshop)
    async def create_workshop(workshop: Annotated[schemas.CreateWorkshop, Form()], db: AsyncSession = Depends(get_db)):
        check_workshop = await WorkshopsOperations.get_workshops(db)
        if workshop.name in [item.name for item in check_workshop]:
            raise HTTPException(status_code=400, detail='Цех с таким названием уже существует')

        try:
            db_workshop = await WorkshopsOperations.create_workshop(db, workshop)
        except:
            raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

        return db_workshop

    # PATCH для обновления цеха
    @workshops_router.patch('/{workshop_id}', response_model=dict)
    async def update_workshop(workshop: Annotated[schemas.UpdateWorkshop, Form()], db: AsyncSession = Depends(get_db)):
        db_workshops = await WorkshopsOperations.get_workshops(db)
        if workshop.id not in [item.id for item in db_workshops]:
            raise HTTPException(status_code=404, detail="Цех не найден")
        
        try:
            await WorkshopsOperations.update_workshop(db, workshop.id, workshop)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")
        
        return {'detail': 'Цех успешно изменен'}

    # DELETE для удаления цеха
    @workshops_router.delete('/{workshop_id}', response_model=dict)
    async def delete_workshop(workshop_id: int, db: AsyncSession = Depends(get_db)):
        db_workshops = await WorkshopsOperations.get_workshops(db)
        if workshop_id not in [item.id for item in db_workshops]:
            raise HTTPException(status_code=404, detail="Цех не найден")

        try:
            await WorkshopsOperations.delete_workshop(db, workshop_id)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")

        return {"detail": "Цех успешно удален"}

class LaboratoriesRouter:
    # готово
    @laboratories_router.get('/', response_model=list[schemas.TestLaboratories])
    async def get_laboratories(db: AsyncSession = Depends(get_db)):
        db_laboratories = await LaboratoriesOperations.get_laboratories(db)
        return db_laboratories

    # готово
    @laboratories_router.post('/', response_model=schemas.TestLaboratories)
    async def create_laboratory(laboratory: Annotated[schemas.CreateLaboratory, Form()], db: AsyncSession = Depends(get_db)):
        check_laboratory = await LaboratoriesOperations.get_laboratories(db)
        if laboratory.name in [item.name for item in check_laboratory]:
            raise HTTPException(status_code=400, detail='Лаборатория уже существует')

        try:
            db_laboratory = await LaboratoriesOperations.create_laboratory(db, laboratory)
        except:
            raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

        return db_laboratory

    # готово
    @laboratories_router.get('/{laboratory_name}', response_model=schemas.TestLaboratories)
    async def get_laboratory(laboratory_name: str, db: AsyncSession = Depends(get_db)):
        laboratory = await LaboratoriesOperations.get_laboratory(db, laboratory_name)
        if laboratory is None:
            raise HTTPException(status_code=400, detail='Название лаборатории введено неверно')
        return laboratory

    # PATCH для обновления лаборатории
    @laboratories_router.patch('/{laboratory_id}', response_model=dict)
    async def update_laboratory(laboratory: Annotated[schemas.TestLaboratories, Form()], db: AsyncSession = Depends(get_db)):
        db_laboratory = await LaboratoriesOperations.get_laboratory(db, laboratory.id)
        if db_laboratory is None:
            raise HTTPException(status_code=404, detail="Лаборатория не найдена")
        
        try:
            await LaboratoriesOperations.update_laboratory(db, laboratory.id, laboratory)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")
        
        return {'detail': 'Лаборатория успешно изменена'}

    # DELETE для удаления лаборатории
    @laboratories_router.delete('/{laboratory_id}', response_model=dict)
    async def delete_laboratory(laboratory_id: int, db: AsyncSession = Depends(get_db)):
        db_laboratory = await LaboratoriesOperations.get_laboratory(db, laboratory_id)
        if db_laboratory is None:
            raise HTTPException(status_code=404, detail="Лаборатория не найдена")

        try:
            await LaboratoriesOperations.delete_laboratory(db, laboratory_id)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")

        return {"detail": "Лаборатория успешно удалена"}

class PersonalLaboratoriesRouter:
    # готово
    @personal_laboratories_router.get('/', response_model=list[schemas.PersonalLaboratories])
    async def get_personal_laboratories(db: AsyncSession = Depends(get_db)):
        db_personal = await PersonalLaboratoriesOperations.get_personal_laboratories(db)
        if not db_personal:
            raise HTTPException(status_code=400, detail='Работников для лабораторий не существует')

        return db_personal

    # готово
    @personal_laboratories_router.post('/', response_model=schemas.PersonalLaboratories)
    async def create_person_laboratory(person: Annotated[schemas.CreatePersonalLaboratory, Form()], db: AsyncSession = Depends(get_db)):
        try:
            db_person = await PersonalLaboratoriesOperations.create_person_laboratory(db, person)
        except:
            raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

        return db_person

    # готово
    @personal_laboratories_router.get('/{person_id}', response_model=schemas.PersonalLaboratories)
    async def get_person_laboratory(person_id: int, db: AsyncSession = Depends(get_db)):
        db_person = await PersonalLaboratoriesOperations.get_person_laboratory(db, person_id)
        if not db_person:
            raise HTTPException(status_code=400, detail='Работника с таким id не существует')

        return db_person

    # PATCH для обновления персонала лаборатории
    @personal_laboratories_router.patch('/{person_id}', response_model=dict)
    async def update_personal_laboratory(person: Annotated[schemas.UpdatePersonalLaboratory, Form()], db: AsyncSession = Depends(get_db)):
        db_person = await PersonalLaboratoriesOperations.get_person_laboratory(db, person.id)
        if db_person is None:
            raise HTTPException(status_code=404, detail="Работник лаборатории не найден")
        
        try:
            await PersonalLaboratoriesOperations.update_personal_laboratory(db, person.id, person)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")
        
        return {'detail': 'Работник лаборатории успешно изменен'}

    # DELETE для удаления персонала лаборатории
    @personal_laboratories_router.delete('/{person_id}', response_model=dict)
    async def delete_personal_laboratory(person_id: int, db: AsyncSession = Depends(get_db)):
        db_person = await PersonalLaboratoriesOperations.get_person_laboratory(db, person_id)
        if db_person is None:
            raise HTTPException(status_code=404, detail="Работник лаборатории не найден")

        try:
            await PersonalLaboratoriesOperations.delete_person_laboratory(db, person_id)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")

        return {"detail": "Работник лаборатории успешно удален"}

class ToolsRouter:
    # готово
    @tools_router.get('/', response_model=list[schemas.Tools])
    async def get_tools(db: AsyncSession = Depends(get_db)):
        tools = await ToolsOperations.get_tools(db)
        if not tools:
            raise HTTPException(status_code=400, detail='Инструментов не существует')

        return tools

    # готово
    @tools_router.post('/', response_model=schemas.Tools)
    async def create_tool(tool: Annotated[schemas.CreateTool, Form()], db: AsyncSession = Depends(get_db)):
        try:
            db_tool = await ToolsOperations.create_tools(db, tool)
        except:
            raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

        return db_tool

    # PATCH для обновления инструмента
    @tools_router.patch('/{tool_id}', response_model=dict)
    async def update_tool(tool: Annotated[schemas.UpdateTool, Form()], db: AsyncSession = Depends(get_db)):
        db_tools = await ToolsOperations.get_tools(db)
        if tool.id not in [item.id for item in db_tools]:
            raise HTTPException(status_code=404, detail="Инструмент не найден")
        
        try:
            await ToolsOperations.update_tool(db, tool.id, tool)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")
        
        return {'detail': 'Инструмент успешно изменен'}

    # DELETE для удаления инструмента
    @tools_router.delete('/{tool_id}', response_model=dict)
    async def delete_tool(tool_id: int, db: AsyncSession = Depends(get_db)):
        db_tools = await ToolsOperations.get_tools(db)
        if tool_id not in [item.id for item in db_tools]:
            raise HTTPException(status_code=404, detail="Инструмент не найден")

        try:
            await ToolsOperations.delete_tool(db, tool_id)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")

        return {"detail": "Инструмент успешно удален"}

class WorksWithProductRouter:
    # готово
    @works_with_product_router.get('/', response_model=list[schemas.WorksWithProduct])
    async def get_works_for_product(db: AsyncSession = Depends(get_db)):
        db_works = await WorksWithProductOperations.get_works_with_product(db)
        if not db_works:
            raise HTTPException(status_code=400, detail='Работ для продуктов не существует')

        return db_works

    # готово
    @works_with_product_router.post('/', response_model=schemas.WorksWithProduct)
    async def create_work_for_product(work: Annotated[schemas.CreateWorkForProduct, Form()], db: AsyncSession = Depends(get_db)):
        check_work = await WorksWithProductOperations.get_works_with_product(db)
        if work.name in [item.name for item in check_work]:
            raise HTTPException(status_code=400, detail='Работа для продукта с таким названием уже существует')

        try:
            db_work = await WorksWithProductOperations.create_work_for_product(db, work)
        except:
            raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

        return db_work

    # PATCH для обновления работы с продуктом
    @works_with_product_router.patch('/{work_id}', response_model=dict)
    async def update_work_with_product(work: Annotated[schemas.UpdateWorkForProduct, Form()], db: AsyncSession = Depends(get_db)):
        db_works = await WorksWithProductOperations.get_works_with_product(db)
        if work.id not in [item.id for item in db_works]:
            raise HTTPException(status_code=404, detail="Работа с продуктом не найдена")
        
        try:
            await WorksWithProductOperations.update_work_with_product(db, work.id, work)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")
        
        return {'detail': 'Работа с продуктом успешно изменена'  }

    # DELETE для удаления работы с продуктом
    @works_with_product_router.delete('/{work_id}', response_model=dict)
    async def delete_work_with_product(work_id: int, db: AsyncSession = Depends(get_db)):
        db_works = await WorksWithProductOperations.get_works_with_product(db)
        if work_id not in [item.id for item in db_works]:
            raise HTTPException(status_code=404, detail="Работа с продуктом не найдена")

        try:
            await WorksWithProductOperations.delete_work_with_product(db, work_id)
        except:
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")

        return {"detail": "Работа с продуктом успешно удалена"}
