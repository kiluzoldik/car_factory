from pydantic import BaseModel
from datetime import datetime


class ProductBase(BaseModel):
    name: str

class PersonalBase(BaseModel):
    full_name: str
    birthday: str
    status: str

class Product(ProductBase):
    count: int
    process_start: datetime
    process_finish: datetime | None = None
    product_category_id: int
    laboratory_id: int | None = None

    class Config:
        from_attributes = True

class CreateProduct(Product):
    pass

class ProductCategory(ProductBase):
    products: list[Product] = []

    class Config:
        from_attributes = True

class CreateProductCategory(ProductCategory):
    pass

class PersonalCategory(ProductBase):
    pass

class CreatePersonalCategory(ProductBase):
    pass

class EngineerPersonal(PersonalBase):
    personal_category_id: int
    workshop_id: int

    class Config:
        from_attributes = True

class CreateEngineerPersonal(EngineerPersonal):
    pass

class PersonalWorkers(PersonalBase):
    personal_category_id: int
    workshop_id: int

    class Config:
        from_attributes = True

class CreatePersonalWorkers(PersonalWorkers):
    pass

class PersonalLaboratories(PersonalBase):
    laboratory_id: int

    class Config:
        from_attributes = True

class CreatePersonalLaboratory(PersonalLaboratories):
    pass

class Brigades(ProductBase):
    workshop_id: int
    product_id: int
    peoples: list[PersonalWorkers | EngineerPersonal | PersonalLaboratories] = []

    class Config:
        from_attributes = True

class CreateBrigades(Brigades):
    pass

class Workshop(ProductBase):
    product_category_id: int

    class Config:
        from_attributes = True

class CreateWorkshop(Workshop):
    pass

class TestLaboratories(BaseModel):
    id: int
    name: str
    test_date_start: datetime
    test_date_finish: datetime | None = None

    class Config:
        from_attributes = True

class CreateLaboratory(ProductBase):
    pass

class Tools(ProductBase):
    laboratory_id: int

    class Config:
        from_attributes = True

class CreateTool(Tools):
    pass

class WorksWithProduct(ProductBase):
    product_id: int

    class Config:
        from_attributes = True

class CreateWorkForProduct(WorksWithProduct):
    pass