from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import src.models as models
from src.schemas import CreateProduct, CreateProductCategory, CreatePersonalCategory, CreateLaboratory, \
    CreateEngineerPersonal, CreateWorkshop, CreatePersonalWorkers, CreateBrigades, CreateTool, CreateWorkForProduct, \
    CreatePersonalLaboratory, PersonalCategory, ProductCategory, TestLaboratories, UpdateBrigades, UpdateEngineerPersonal, UpdatePersonalLaboratory, UpdatePersonalWorkers, UpdateProduct, UpdateTool, UpdateWorkForProduct, UpdateWorkshop


# готово
async def get_product(db: AsyncSession, product_name: str):
    result = await db.execute(select(models.Product).filter_by(name=product_name))
    return result.scalars().first()

# готово
async def create_product(db: AsyncSession, product: CreateProduct):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def update_product(db: AsyncSession, product_id: int, product_data: UpdateProduct):
    db_product = await db.execute(select(models.Product).filter_by(id=product_id))
    product = db_product.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail='Продукт с таким id не существует')
    
    update_product = product_data.model_dump(exclude_unset=True)
    
    for field, value in update_product.items():
        setattr(product, field, value)
        
    await db.commit()
    await db.refresh(product)
    return product

async def delete_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(models.Product).filter_by(id=product_id))
    db_product = result.scalars().first()
    if not db_product:
        raise HTTPException(status_code=404, detail='Продукт с таким id не существует')
    
    await db.delete(db_product)
    await db.commit()
    return {'detail': 'Продукт успешно удален'}

# готово
async def get_products(db: AsyncSession):
    result = await db.execute(select(models.Product))
    return result.scalars().all()

# готово
async def get_product_categories(db: AsyncSession):
    result = await db.execute(select(models.ProductCategory))
    return result.scalars().all()

# готово
async def create_product_category(db: AsyncSession, category: CreateProductCategory):
    db_category = models.ProductCategory(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def update_product_category(db: AsyncSession, category_id: int, category_data: ProductCategory):
    db_category = await db.execute(select(models.ProductCategory).filter_by(id=category_id))
    category = db_category.scalars().first()
    update_data = category_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(category, field, value)

    await db.commit()
    await db.refresh(category)
    return category

async def delete_product_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(models.ProductCategory).filter_by(id=category_id))
    db_category = result.scalars().first()

    await db.delete(db_category)
    await db.commit()
    return {'detail': 'Категория продукта успешно удалена'}

# готово
async def get_personal_categories(db: AsyncSession):
    result = await db.execute(select(models.PersonalCategory))
    return result.scalars().all()

# готово
async def create_personal_category(db: AsyncSession, category: CreatePersonalCategory):
    db_category = models.PersonalCategory(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def update_personal_category(db: AsyncSession, category_id: int, category_data: PersonalCategory):
    db_category = await db.execute(select(models.PersonalCategory).filter_by(id=category_id))
    category = db_category.scalars().first()
    update_data = category_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(category, field, value)

    await db.commit()
    await db.refresh(category)
    return category

async def delete_personal_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(PersonalCategory).filter_by(id=category_id))
    db_category = result.scalars().first()

    await db.delete(db_category)
    await db.commit()
    return {'detail': 'Категория персонала успешно удалена'}

# готово
async def get_engineer_personal(db: AsyncSession):
    result = await db.execute(select(models.EngineerPersonal))
    return result.scalars().all()

# готово
async def create_engineer_personal(db: AsyncSession, personal: CreateEngineerPersonal):
    db_personal = models.EngineerPersonal(**personal.model_dump())
    db.add(db_personal)
    await db.commit()
    await db.refresh(db_personal)
    return db_personal

# готово
async def get_engineer_person(db: AsyncSession, person_id: int):
    result = await db.execute(select(models.EngineerPersonal).filter_by(id=person_id))
    return result.scalars().first()

async def update_engineer_personal(db: AsyncSession, person_id: int, personal_data: UpdateEngineerPersonal):
    db_personal = await db.execute(select(models.EngineerPersonal).filter_by(id=person_id))
    personal = db_personal.scalars().first()
    update_data = personal_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(personal, field, value)

    await db.commit()
    await db.refresh(personal)
    return personal

async def delete_engineer_personal(db: AsyncSession, person_id: int):
    result = await db.execute(select(models.EngineerPersonal).filter_by(id=person_id))
    db_personal = result.scalars().first()

    await db.delete(db_personal)
    await db.commit()
    return {'detail': 'Инженер успешно удален'}

# готово
async def get_personal_workers(db: AsyncSession):
    workers = await db.execute(select(models.PersonalWorkers))
    return workers.scalars().all()

# готово
async def create_personal_worker(db: AsyncSession, worker: CreatePersonalWorkers):
    worker = models.PersonalWorkers(**worker.model_dump())
    db.add(worker)
    await db.commit()
    await db.refresh(worker)
    return worker

# готово
async def get_personal_worker(db: AsyncSession, person_id: int):
    worker = await db.execute(select(models.PersonalWorkers).filter_by(id=person_id))
    return worker.scalars().first()

async def update_personal_worker(db: AsyncSession, worker_id: int, worker_data: UpdatePersonalWorkers):
    db_worker = await db.execute(select(models.PersonalWorkers).filter_by(id=worker_id))
    worker = db_worker.scalars().first()
    update_data = worker_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(worker, field, value)

    await db.commit()
    await db.refresh(worker)
    return worker

async def delete_personal_worker(db: AsyncSession, worker_id: int):
    result = await db.execute(select(models.PersonalWorkers).filter_by(id=worker_id))
    db_worker = result.scalars().first()

    await db.delete(db_worker)
    await db.commit()
    return {'detail': 'Работник успешно удален'}

# готово
async def get_brigades(db: AsyncSession):
    brigades = await db.execute(select(models.Brigades))
    return brigades.scalars().all()

# готово
async def create_brigade(db: AsyncSession, brigade: CreateBrigades):
    brigade = models.Brigades(**brigade.model_dump())
    db.add(brigade)
    await db.commit()
    await db.refresh(brigade)
    return brigade

# готово
async def get_brigade(db: AsyncSession, brigade_id: int):
    brigade = await db.execute(select(models.Brigades).filter_by(id=brigade_id))
    return brigade.scalars().first()

async def update_brigade(db: AsyncSession, brigade_id: int, brigade_data: UpdateBrigades):
    db_brigade = await db.execute(select(models.Brigades).filter_by(id=brigade_id))
    brigade = db_brigade.scalars().first()
    update_data = brigade_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(brigade, field, value)

    await db.commit()
    await db.refresh(brigade)
    return brigade

async def delete_brigade(db: AsyncSession, brigade_id: int):
    result = await db.execute(select(models.Brigades).filter_by(id=brigade_id))
    db_brigade = result.scalars().first()

    await db.delete(db_brigade)
    await db.commit()
    return {'detail': 'Бригада успешно удалена'}

# готово
async def get_workshops(db: AsyncSession):
    workshops = await db.execute(select(models.Workshop))
    return workshops.scalars().all()

# готово
async def create_workshop(db: AsyncSession, workshop: CreateWorkshop):
    db_workshop = models.Workshop(**workshop.model_dump())
    db.add(db_workshop)
    await db.commit()
    await db.refresh(db_workshop)
    return db_workshop

async def update_workshop(db: AsyncSession, workshop_id: int, workshop_data: UpdateWorkshop):
    db_workshop = await db.execute(select(models.Workshop).filter_by(id=workshop_id))
    workshop = db_workshop.scalars().first()
    if not workshop:
        raise HTTPException(status_code=404, detail='Цех с таким id не существует')

    update_data = workshop_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(workshop, field, value)

    await db.commit()
    await db.refresh(workshop)
    return workshop

async def delete_workshop(db: AsyncSession, workshop_id: int):
    result = await db.execute(select(models.Workshop).filter_by(id=workshop_id))
    db_workshop = result.scalars().first()
    if not db_workshop:
        raise HTTPException(status_code=404, detail='Цех с таким id не существует')

    await db.delete(db_workshop)
    await db.commit()
    return {'detail': 'Цех успешно удален'}

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
    db.add(db_laboratory)
    await db.commit()
    await db.refresh(db_laboratory)
    return db_laboratory

async def update_laboratory(db: AsyncSession, laboratory_id: int, laboratory_data: TestLaboratories):
    db_laboratory = await db.execute(select(models.TestLaboratories).filter_by(id=laboratory_id))
    laboratory = db_laboratory.scalars().first()
    update_data = laboratory_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(laboratory, field, value)

    await db.commit()
    await db.refresh(laboratory)
    return laboratory

async def delete_laboratory(db: AsyncSession, laboratory_id: int):
    result = await db.execute(select(models.TestLaboratories).filter_by(id=laboratory_id))
    db_laboratory = result.scalars().first()

    await db.delete(db_laboratory)
    await db.commit()
    return {'detail': 'Лаборатория успешно удалена'}

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
    db.add(add_person)
    await db.commit()
    await db.refresh(add_person)
    return add_person

async def update_personal_laboratory(db: AsyncSession, person_id: int, personal_data: UpdatePersonalLaboratory):
    db_personal = await db.execute(select(models.PersonalLaboratories).filter_by(id=person_id))
    personal = db_personal.scalars().first()
    update_data = personal_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(personal, field, value)

    await db.commit()
    await db.refresh(personal)
    return personal

async def delete_personal_laboratory(db: AsyncSession, person_id: int):
    result = await db.execute(select(models.PersonalLaboratories).filter_by(id=person_id))
    db_personal = result.scalars().first()

    await db.delete(db_personal)
    await db.commit()
    return {'detail': 'Персонал лаборатории успешно удален'}

# готово
async def get_tools(db: AsyncSession):
    tools = await db.execute(select(models.Tools))
    return tools.scalars().all()

# готово
async def create_tools(db: AsyncSession, tool: CreateTool):
    add_tool = models.Tools(**tool.model_dump())
    db.add(add_tool)
    await db.commit()
    await db.refresh(add_tool)
    return add_tool

async def update_tool(db: AsyncSession, tool_id: int, tool_data: UpdateTool):
    db_tool = await db.execute(select(models.Tools).filter_by(id=tool_id))
    tool = db_tool.scalars().first()
    update_data = tool_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(tool, field, value)

    await db.commit()
    await db.refresh(tool)
    return tool

async def delete_tool(db: AsyncSession, tool_id: int):
    result = await db.execute(select(models.Tools).filter_by(id=tool_id))
    db_tool = result.scalars().first()

    await db.delete(db_tool)
    await db.commit()
    return {'detail': 'Инструмент успешно удален'}

# готово
async def get_works_with_product(db: AsyncSession):
    works = await db.execute(select(models.WorksWithProduct))
    return works.scalars().all()

# готово
async def create_work_for_product(db: AsyncSession, work: CreateWorkForProduct):
    add_work = models.WorksWithProduct(**work.model_dump())
    db.add(add_work)
    await db.commit()
    await db.refresh(add_work)
    return add_work

async def update_work_with_product(db: AsyncSession, work_id: int, work_data: UpdateWorkForProduct):
    db_work = await db.execute(select(models.WorksWithProduct).filter_by(id=work_id))
    work = db_work.scalars().first()
    update_data = work_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(work, field, value)

    await db.commit()
    await db.refresh(work)
    return work

async def delete_work_with_product(db: AsyncSession, work_id: int):
    result = await db.execute(select(models.WorksWithProduct).filter_by(id=work_id))
    db_work = result.scalars().first()

    await db.delete(db_work)
    await db.commit()
    return {'detail': 'Работа для продукта успешно удалена'}
