from pydantic import BaseModel
from datetime import datetime


class Product(BaseModel):
    id: int
    name: str
    count: int
    process_start: datetime
    process_finish: datetime | None = None
    product_category_id: int
    laboratory_id: int | None = None

    class Config:
        from_attributes = True

class CreateProduct(BaseModel):
    name: str
    count: int
    product_category_id: int
    laboratory_id: int | None = None

class ProductCategory(BaseModel):
    id: int
    name: str
    #products: list[Product] = []

    class Config:
        from_attributes = True

class CreateProductCategory(BaseModel):
    name: str

class PersonalCategory(BaseModel):
    id: int
    name: str

class CreatePersonalCategory(BaseModel):
    name: str

class EngineerPersonal(BaseModel):
    id: int
    full_name: str
    birthday: str
    status: str
    personal_category_id: int
    workshop_id: int

    class Config:
        from_attributes = True

class CreateEngineerPersonal(BaseModel):
    full_name: str
    birthday: str
    status: str
    personal_category_id: int
    workshop_id: int

class PersonalWorkers(BaseModel):
    id: int
    full_name: str
    birthday: str
    status: str
    personal_category_id: int
    workshop_id: int

    class Config:
        from_attributes = True

class CreatePersonalWorkers(BaseModel):
    full_name: str
    birthday: str
    status: str
    personal_category_id: int
    workshop_id: int

class PersonalLaboratories(BaseModel):
    id: int
    full_name: str
    birthday: str
    status: str
    laboratory_id: int

    class Config:
        from_attributes = True

class CreatePersonalLaboratory(BaseModel):
    full_name: str
    birthday: str
    status: str
    laboratory_id: int

class Brigades(BaseModel):
    id: int
    name: str
    workshop_id: int
    product_id: int
    # peoples: list[PersonalWorkers | EngineerPersonal | PersonalLaboratories] = []

    class Config:
        from_attributes = True

class CreateBrigades(BaseModel):
    name: str
    workshop_id: int
    product_id: int

class Workshop(BaseModel):
    id: int
    name: str
    product_category_id: int

    class Config:
        from_attributes = True

class CreateWorkshop(BaseModel):
    name: str
    product_category_id: int

class TestLaboratories(BaseModel):
    id: int
    name: str
    test_date_start: datetime
    test_date_finish: datetime | None = None

    class Config:
        from_attributes = True

class CreateLaboratory(BaseModel):
    name: str

class Tools(BaseModel):
    id: int
    name: str
    laboratory_id: int

    class Config:
        from_attributes = True

class CreateTool(BaseModel):
    name: str
    laboratory_id: int

class WorksWithProduct(BaseModel):
    id: int
    name: str
    product_id: int

    class Config:
        from_attributes = True

class CreateWorkForProduct(BaseModel):
    name: str
    product_id: int