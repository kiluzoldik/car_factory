from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import src.models as models
from .dependencies import db_create, db_delete, db_update
from src.schemas import (CreateProduct, CreateProductCategory, 
                         CreatePersonalCategory, CreateLaboratory,
                         CreateEngineerPersonal, CreateWorkshop, 
                         CreatePersonalWorkers, CreateBrigades,
                         CreateTool, CreateWorkForProduct,
                         CreatePersonalLaboratory, PersonalCategory, 
                         ProductCategory, TestLaboratories, UpdateBrigades,
                         UpdateEngineerPersonal, UpdatePersonalLaboratory, 
                         UpdatePersonalWorkers, UpdateProduct, UpdateTool, 
                         UpdateWorkForProduct, UpdateWorkshop)


# Класс реализовывающий CRUD для продуктов
class ProductOperations:
    # готово
    async def get_product(db: AsyncSession, product_id: int):
        result = await db.execute(select(models.Product).filter_by(id=product_id))
        return result.scalars().first()

    # готово
    async def create_product(db: AsyncSession, product: CreateProduct):
        db_product = models.Product(**product.model_dump())
        return await db_create(db_product, db)

    async def update_product(db: AsyncSession, product_id: int, product_data: UpdateProduct):
        db_product = await db.execute(select(models.Product).filter_by(id=product_id))
        return await db_update(db_product, db, product_data)

    async def delete_product(db: AsyncSession, product_id: int):
        result = await db.execute(select(models.Product).filter_by(id=product_id))
        return await db_delete(result, db)
    # готово
    async def get_products(db: AsyncSession):
        result = await db.execute(select(models.Product))
        
        return result.scalars().all()

# Класс реализовывающий CRUD для категорий продуктов
class ProductCategoryOperations:
    # готово
    async def get_product_categories(db: AsyncSession):
        result = await db.execute(select(models.ProductCategory))
        return result.scalars().all()

    # готово
    async def create_product_category(db: AsyncSession, category: CreateProductCategory):
        db_category = models.ProductCategory(**category.model_dump())
        return await db_create(db_category, db)

    async def update_product_category(db: AsyncSession, category_id: int, category_data: ProductCategory):
        db_category = await db.execute(select(models.ProductCategory).filter_by(id=category_id))
        return await db_update(db_category, db, category_data)

    async def delete_product_category(db: AsyncSession, category_id: int):
        result = await db.execute(select(models.ProductCategory).filter_by(id=category_id))
        return await db_delete(result, db)

# Класс реализовывающий CRUD для категорий персонала
class PersonalCategoryOperations:
    # готово
    async def get_personal_categories(db: AsyncSession):
        result = await db.execute(select(models.PersonalCategory))
        return result.scalars().all()

    # готово
    async def create_personal_category(db: AsyncSession, category: CreatePersonalCategory):
        db_category = models.PersonalCategory(**category.model_dump())
        return await db_create(db_category, db)
    
    async def update_personal_category(db: AsyncSession, category_id: int, category_data: PersonalCategory):
        db_category = await db.execute(select(models.PersonalCategory).filter_by(id=category_id))
        return await db_update(db_category, db, category_data)

    async def delete_personal_category(db: AsyncSession, category_id: int):
        result = await db.execute(select(PersonalCategory).filter_by(id=category_id))
        return await db_delete(result, db)

# Класс реализовывающий CRUD для инженерного персонала
class EngineerPersonalOperations:
    # готово
    async def get_engineer_personal(db: AsyncSession):
        result = await db.execute(select(models.EngineerPersonal))
        return result.scalars().all()

    # готово
    async def create_engineer_personal(db: AsyncSession, personal: CreateEngineerPersonal):
        db_personal = models.EngineerPersonal(**personal.model_dump())
        return await db_create(db_personal, db)

    # готово
    async def get_engineer_person(db: AsyncSession, person_id: int):
        result = await db.execute(select(models.EngineerPersonal).filter_by(id=person_id))
        return result.scalars().first()

    async def update_engineer_personal(db: AsyncSession, person_id: int, personal_data: UpdateEngineerPersonal):
        db_personal = await db.execute(select(models.EngineerPersonal).filter_by(id=person_id))
        return await db_update(db_personal, db, personal_data)

    async def delete_engineer_personal(db: AsyncSession, person_id: int):
        result = await db.execute(select(models.EngineerPersonal).filter_by(id=person_id))
        return await db_delete(result, db)

# Класс реализовывающий CRUD для обычного персонала
class PersonalWorkersOperations:
    # готово
    async def get_personal_workers(db: AsyncSession):
        workers = await db.execute(select(models.PersonalWorkers))
        return workers.scalars().all()

    # готово
    async def create_personal_worker(db: AsyncSession, worker: CreatePersonalWorkers):
        worker = models.PersonalWorkers(**worker.model_dump())
        return await db_create(worker, db)

    # готово
    async def get_personal_worker(db: AsyncSession, person_id: int):
        worker = await db.execute(select(models.PersonalWorkers).filter_by(id=person_id))
        return worker.scalars().first()

    async def update_personal_worker(db: AsyncSession, worker_id: int, worker_data: UpdatePersonalWorkers):
        db_worker = await db.execute(select(models.PersonalWorkers).filter_by(id=worker_id))
        return await db_update(db_worker, db, worker_data)

    async def delete_personal_worker(db: AsyncSession, worker_id: int):
        result = await db.execute(select(models.PersonalWorkers).filter_by(id=worker_id))
        return await db_delete(result, db)

# Класс реализовывающий CRUD для бригад
class BrigadesOperations:
    # готово
    async def get_brigades(db: AsyncSession):
        brigades = await db.execute(select(models.Brigades))
        return brigades.scalars().all()

    # готово
    async def create_brigade(db: AsyncSession, brigade: CreateBrigades):
        brigade = models.Brigades(**brigade.model_dump())
        return await db_create(brigade, db)

    # готово
    async def get_brigade(db: AsyncSession, brigade_id: int):
        brigade = await db.execute(select(models.Brigades).filter_by(id=brigade_id))
        return brigade.scalars().first()

    async def update_brigade(db: AsyncSession, brigade_id: int, brigade_data: UpdateBrigades):
        db_brigade = await db.execute(select(models.Brigades).filter_by(id=brigade_id))
        return await db_update(db_brigade, db, brigade_data)

    async def delete_brigade(db: AsyncSession, brigade_id: int):
        result = await db.execute(select(models.Brigades).filter_by(id=brigade_id))
        return await db_delete(result, db)

# Класс реализовывающий CRUD для цехов
class WorkshopsOperations:
    # готово
    async def get_workshops(db: AsyncSession):
        workshops = await db.execute(select(models.Workshop))
        return workshops.scalars().all()

    # готово
    async def create_workshop(db: AsyncSession, workshop: CreateWorkshop):
        db_workshop = models.Workshop(**workshop.model_dump())
        return await db_create(db_workshop, db)

    async def update_workshop(db: AsyncSession, workshop_id: int, workshop_data: UpdateWorkshop):
        db_workshop = await db.execute(select(models.Workshop).filter_by(id=workshop_id))
        return await db_update(db_workshop, db, workshop_data)

    async def delete_workshop(db: AsyncSession, workshop_id: int):
        result = await db.execute(select(models.Workshop).filter_by(id=workshop_id))
        return await db_delete(result, db)

# Класс реализовывающий CRUD для лабораторий
class LaboratoriesOperations:
    # готово
    async def get_laboratories(db: AsyncSession):
        result = await db.execute(select(models.TestLaboratories))
        return result.scalars().all()

    # готово
    async def get_laboratory(db: AsyncSession, laboratory_id: int):
        result = await db.execute(select(models.TestLaboratories).filter_by(id=laboratory_id))
        return result.scalars().first()

    # готово
    async def create_laboratory(db: AsyncSession, laboratory: CreateLaboratory):
        db_laboratory = models.TestLaboratories(**laboratory.model_dump())
        return await db_create(db_laboratory, db)

    async def update_laboratory(db: AsyncSession, laboratory_id: int, laboratory_data: TestLaboratories):
        db_laboratory = await db.execute(select(models.TestLaboratories).filter_by(id=laboratory_id))
        return await db_update(db_laboratory, db, laboratory_data)

    async def delete_laboratory(db: AsyncSession, laboratory_id: int):
        result = await db.execute(select(models.TestLaboratories).filter_by(id=laboratory_id))
        return await db_delete(result, db)

# Класс реализовывающий CRUD для персональных лабораторий
class PersonalLaboratoriesOperations:
    # готово
    async def get_personal_laboratories(db: AsyncSession):
        personal = await db.execute(select(models.PersonalLaboratories))
        return personal.scalars().all()

    # готово
    async def get_person_laboratory(db: AsyncSession, person_id: int):
        person = await db.execute(select(models.PersonalLaboratories).filter_by(id=person_id))
        return person.scalars().first()

    # готово
    async def create_person_laboratory(db: AsyncSession, person: CreatePersonalLaboratory):
        add_person = models.PersonalLaboratories(**person.model_dump())
        return await db_create(add_person, db)

    async def update_personal_laboratory(db: AsyncSession, person_id: int, personal_data: UpdatePersonalLaboratory):
        db_personal = await db.execute(select(models.PersonalLaboratories).filter_by(id=person_id))
        return await db_update(db_personal, db, personal_data)

    async def delete_personal_laboratory(db: AsyncSession, person_id: int):
        result = await db.execute(select(models.PersonalLaboratories).filter_by(id=person_id))
        return await db_delete(result, db)

# Класс реализовывающий CRUD для инструментов
class ToolsOperations:
    # готово
    async def get_tools(db: AsyncSession):
        tools = await db.execute(select(models.Tools))
        return tools.scalars().all()

    # готово
    async def create_tools(db: AsyncSession, tool: CreateTool):
        add_tool = models.Tools(**tool.model_dump())
        return await db_create(add_tool, db)

    async def update_tool(db: AsyncSession, tool_id: int, tool_data: UpdateTool):
        db_tool = await db.execute(select(models.Tools).filter_by(id=tool_id))
        return await db_update(db_tool, db, tool_data)

    async def delete_tool(db: AsyncSession, tool_id: int):
        result = await db.execute(select(models.Tools).filter_by(id=tool_id))
        return await db_delete(result, db)

# Класс реализовывающий CRUD для работ с продуктами
class WorksWithProductOperations:
    # готово
    async def get_works_with_product(db: AsyncSession):
        works = await db.execute(select(models.WorksWithProduct))
        return works.scalars().all()

    # готово
    async def create_work_for_product(db: AsyncSession, work: CreateWorkForProduct):
        add_work = models.WorksWithProduct(**work.model_dump())
        return await db_create(add_work, db)

    async def update_work_with_product(db: AsyncSession, work_id: int, work_data: UpdateWorkForProduct):
        db_work = await db.execute(select(models.WorksWithProduct).filter_by(id=work_id))
        return await db_update(db_work, db, work_data)

    async def delete_work_with_product(db: AsyncSession, work_id: int):
        result = await db.execute(select(models.WorksWithProduct).filter_by(id=work_id))
        return await db_delete(result, db)
