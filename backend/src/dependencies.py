from typing import Any, Callable
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession


async def create_func(get_func: Callable, 
                      create_func: Callable, 
                      db: AsyncSession, 
                      something: Any, 
                      entity_name: str):
    
    check = await get_func(db)
    if something.name in [item.name for item in check]:
         raise HTTPException(status_code=400, detail=f'{entity_name} уже существует')

    try:
        result = await create_func(db, something)
    except:
        raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

    return result

async def create_func_without_entity_name(create_func: Callable, 
                                          db: AsyncSession, 
                                          something: Any):
    
    try:
        result = await create_func(db, something)
    except:
        raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')

    return result

async def update_func(get_func: Callable, 
                      update_func: Callable, 
                      db: AsyncSession, 
                      something: Any, 
                      entity_name: str):
    
    results = await get_func(db)
    if something.id not in [item.id for item in results]:
        raise HTTPException(status_code=404, detail=f'{entity_name} не найден')
    
    try:
        await update_func(db, something.id, something)
    except:
        raise HTTPException(status_code=500, detail='Ошибка на стороне сервера')
    
    return {'detail': f'{entity_name} успешно изменен' }

async def delete_func(get_func: Callable,
                      del_func: Callable, 
                      db: AsyncSession, 
                      something_id: int,
                      entity_name: str):
    
    results = await get_func(db)
    
    if something_id not in [item.id for item in results]:
        raise HTTPException(status_code=404, detail=f'{entity_name} не найден')
    
    try:
        await del_func(db, something_id)
    except:
        raise HTTPException(status_code=500, detail=f'{entity_name} на стороне сервера')

    return {'detail': f'{entity_name} успешно удален'}

async def db_update(something: Any, db: AsyncSession, something_data: Any):
    result = something.scalars().first()
    update_product = something_data.model_dump(exclude_unset=True)
    
    for field, value in update_product.items():
        setattr(result, field, value)
        
    await db.commit()
    await db.refresh(result)
    
    return result

async def db_delete(something: Any, db: AsyncSession):
    db_product = something.scalars().first()
    await db.delete(db_product)
    await db.commit()
    
    return db_product

async def db_create(something: Any, db: AsyncSession):
    db.add(something)
    await db.commit()
    await db.refresh(something)
    
    return something