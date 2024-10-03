from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Product, ProductCategory, PersonalCategory, EngineerPersonal, TestLaboratories, Workshop, \
    PersonalWorkers, Brigades, Tools, WorksWithProduct, PersonalLaboratories
from src.schemas import CreateProduct, CreateProductCategory, CreatePersonalCategory, CreateLaboratory, \
    CreateEngineerPersonal, CreateWorkshop, CreatePersonalWorkers, CreateBrigades, CreateTool, CreateWorkForProduct, \
    CreatePersonalLaboratory


# готово
async def get_product(db: AsyncSession, product_name: str):
    result = await db.execute(select(Product).filter_by(name=product_name))
    return result.scalars().first()

# готово
async def create_product(db: AsyncSession, product: CreateProduct):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# готово
async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()

# готово
async def get_product_categories(db: AsyncSession):
    result = await db.execute(select(ProductCategory))
    return result.scalars().all()

# готово
async def create_product_category(db: AsyncSession, category: CreateProductCategory):
    db_category = ProductCategory(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

# готово
async def get_personal_categories(db: AsyncSession):
    result = await db.execute(select(PersonalCategory))
    return result.scalars().all()

# готово
async def create_personal_category(db: AsyncSession, category: CreatePersonalCategory):
    db_category = PersonalCategory(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

# готово
async def get_engineer_personal(db: AsyncSession):
    result = await db.execute(select(EngineerPersonal))
    return result.scalars().all()

# готово
async def create_engineer_personal(db: AsyncSession, personal: CreateEngineerPersonal):
    db_personal = EngineerPersonal(**personal.model_dump())
    db.add(db_personal)
    await db.commit()
    await db.refresh(db_personal)
    return db_personal

# готово
async def get_engineer_person(db: AsyncSession, person_id: int):
    result = await db.execute(select(EngineerPersonal).filter_by(id=person_id))
    return result.scalars().first()

# готово
async def get_personal_workers(db: AsyncSession):
    workers = await db.execute(select(PersonalWorkers))
    return workers.scalars().all()

# готово
async def create_personal_worker(db: AsyncSession, worker: CreatePersonalWorkers):
    worker = PersonalWorkers(**worker.model_dump())
    db.add(worker)
    await db.commit()
    await db.refresh(worker)
    return worker

# готово
async def get_personal_worker(db: AsyncSession, person_id: int):
    worker = await db.execute(select(PersonalWorkers).filter_by(id=person_id))
    return worker.scalars().first()

# готово
async def get_brigades(db: AsyncSession):
    brigades = await db.execute(select(Brigades))
    return brigades.scalars().all()

# готово
async def create_brigade(db: AsyncSession, brigade: CreateBrigades):
    brigade = Brigades(**brigade.model_dump())
    db.add(brigade)
    await db.commit()
    await db.refresh(brigade)
    return brigade

# готово
async def get_brigade(db: AsyncSession, brigade_id: int):
    brigade = await db.execute(select(Brigades).filter_by(id=brigade_id))
    return brigade.scalars().first()

# готово
async def get_workshops(db: AsyncSession):
    workshops = await db.execute(select(Workshop))
    return workshops.scalars().all()

# готово
async def create_workshop(db: AsyncSession, workshop: CreateWorkshop):
    db_workshop = Workshop(**workshop.model_dump())
    db.add(db_workshop)
    await db.commit()
    await db.refresh(db_workshop)
    return db_workshop

# готово
async def get_laboratories(db: AsyncSession):
    result = await db.execute(select(TestLaboratories))
    return result.scalars().all()

# готово
async def get_laboratory(db: AsyncSession, laboratory_name: str):
    result = await db.execute(select(TestLaboratories).filter_by(name=laboratory_name))
    return result.scalars().first()

# готово
async def create_laboratory(db: AsyncSession, laboratory: CreateLaboratory):
    db_laboratory = TestLaboratories(**laboratory.model_dump())
    db.add(db_laboratory)
    await db.commit()
    await db.refresh(db_laboratory)
    return db_laboratory

# готово
async def get_personal_laboratories(db: AsyncSession):
    personal = await db.execute(select(PersonalLaboratories))
    return personal.scalars().all()

# готово
async def get_person_laboratory(db: AsyncSession, person_id: int):
    person = await db.execute(select(PersonalLaboratories).filter_by(id=person_id))
    return person.scalars().first()

# готово
async def create_person_laboratory(db: AsyncSession, person: CreatePersonalLaboratory):
    add_person = PersonalLaboratories(**person.model_dump())
    db.add(add_person)
    await db.commit()
    await db.refresh(add_person)
    return add_person

# готово
async def get_tools(db: AsyncSession):
    tools = await db.execute(select(Tools))
    return tools.scalars().all()

# готово
async def create_tools(db: AsyncSession, tool: CreateTool):
    add_tool = Tools(**tool.model_dump())
    db.add(add_tool)
    await db.commit()
    await db.refresh(add_tool)
    return add_tool

# готово
async def get_works_with_product(db: AsyncSession):
    works = await db.execute(select(WorksWithProduct))
    return works.scalars().all()

# готово
async def create_work_for_product(db: AsyncSession, work: CreateWorkForProduct):
    add_work = WorksWithProduct(**work.model_dump())
    db.add(add_work)
    await db.commit()
    await db.refresh(add_work)
    return add_work