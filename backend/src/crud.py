from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.models import Product, ProductCategory, PersonalCategory, EngineerPersonal, TestLaboratories
from src.schemas import CreateProduct, CreateProductCategory, CreatePersonalCategory, CreateLaboratory


async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).filter_by(id=product_id))
    return result.scalars().first()

async def create_product(db: AsyncSession, product: CreateProduct):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()

async def get_product_categories(db: AsyncSession):
    result = await db.execute(select(ProductCategory))
    return result.scalars().all()

async def create_product_category(db: AsyncSession, category: CreateProductCategory):
    db_category = ProductCategory(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def get_personal_categories(db: AsyncSession):
    result = await db.execute(select(PersonalCategory))
    return result.scalars().all()

async def create_personal_category(db: AsyncSession, category: CreatePersonalCategory):
    db_category = PersonalCategory(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def get_engineer_personal(db: AsyncSession):
    result = await db.execute(select(EngineerPersonal))
    return result.scalars().all()

async def create_engineer_personal(db: AsyncSession, personal: CreatePersonalCategory):
    db_personal = EngineerPersonal(**personal.model_dump())
    db.add(db_personal)
    await db.commit()
    await db.refresh(db_personal)
    return db_personal

async def get_engineer_person(db: AsyncSession, person_id: int):
    result = await db.execute(select(EngineerPersonal).filter_by(id=person_id))
    return result.scalars().first()

async def get_personal_workers(db: Session, skip: 0, limit: 20):
    pass

async def get_personal_worker(db: Session, person_id: int):
    pass

async def get_brigades(db: Session, skip: 0, limit: 20):
    pass

async def get_brigade(db: Session, brigade_id: int):
    pass

async def get_workshops(db: Session, skip: 0, limit: 20):
    pass

async def get_workshop(db: Session, workshop_id: int):
    pass

async def get_laboratories(db: AsyncSession):
    result = await db.execute(select(TestLaboratories))
    return result.scalars().all()

async def get_laboratory(db: AsyncSession, laboratory_id: int):
    result = await db.execute(select(TestLaboratories).filter_by(id=laboratory_id))
    return result.scalars().first()

async def create_laboratory(db: AsyncSession, laboratory: CreateLaboratory):
    db_laboratory = TestLaboratories(**laboratory.model_dump())
    db.add(db_laboratory)
    await db.commit()
    await db.refresh(db_laboratory)
    return db_laboratory

async def get_personal_laboratories(db: Session, skip: 0, limit: 20):
    pass

async def get_person_laboratory(db: Session, person_id: int):
    pass

async def get_tools(db: Session, skip: 0, limit: 20):
    pass

async def get_works_with_product(db: Session, product_id: int, skip: 0, limit: 20):
    pass