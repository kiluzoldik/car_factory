from datetime import datetime
from sqlalchemy import ForeignKey, text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated

from src.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]

class Product(Base):
    '''Таблица описывающая продукт'''
    
    __tablename__ = 'product'

    id: Mapped[intpk]
    name: Mapped[str]
    count: Mapped[int] = mapped_column(nullable=True)
    process_start: Mapped[datetime] = mapped_column(DateTime, server_default=text('NOW()'))
    process_finish: Mapped[str | None]
    product_category_id: Mapped[int] = mapped_column(ForeignKey('product_category.id', ondelete='CASCADE'))
    laboratory_id: Mapped[int | None] = mapped_column(ForeignKey('test_laboratories.id'))

    product_category = relationship('ProductCategory', back_populates='products')
    laboratory = relationship('TestLaboratories', back_populates='products')
    works_for_product = relationship('WorksWithProduct', back_populates='product', cascade="all, delete")

class ProductCategory(Base):
    '''Таблица описывающая категорию продукта'''

    __tablename__ = 'product_category'

    id: Mapped[intpk]
    name: Mapped[str]

    products = relationship('Product', back_populates='product_category')
    workshop = relationship('Workshop', back_populates='product_category')

class PersonalCategory(Base):
    '''Таблица описывающая категорию персонала'''
    
    __tablename__ = 'personal_category'

    id: Mapped[intpk]
    name: Mapped[str]

    eng_personal = relationship('EngineerPersonal', back_populates='personal_category')

class EngineerPersonal(Base):
    '''Таблица описывающая персонала инженеров'''

    __tablename__ = 'engineer_personal'

    id: Mapped[intpk]
    full_name: Mapped[str]
    birthday: Mapped[str]
    status: Mapped[str]
    personal_category_id: Mapped[int] = mapped_column(ForeignKey('personal_category.id', ondelete="CASCADE"))
    workshop_id: Mapped[int] = mapped_column(ForeignKey('workshop.id'))

    personal_category = relationship('PersonalCategory', back_populates='eng_personal')
    workshop = relationship('Workshop', back_populates='eng_personal')

class PersonalWorkers(Base):
    '''Таблица описывающая персонал работников'''

    __tablename__ = 'personal_workers'

    id: Mapped[intpk]
    full_name: Mapped[str]
    birthday: Mapped[str]
    status: Mapped[str]
    personal_category_id: Mapped[int] = mapped_column(ForeignKey('personal_category.id', ondelete="CASCADE"))
    workshop_id: Mapped[int] = mapped_column(ForeignKey('workshop.id'))

class Brigades(Base):
    '''Таблица описывающая бригады'''

    __tablename__ = 'brigades'

    id: Mapped[intpk]
    name: Mapped[str]
    workshop_id: Mapped[int] = mapped_column(ForeignKey('workshop.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'))

class Workshop(Base):
    '''Таблица описывающая цеха'''

    __tablename__ = 'workshop'

    id: Mapped[intpk]
    name: Mapped[str]
    product_category_id: Mapped[int] = mapped_column(ForeignKey('product_category.id', ondelete="CASCADE"))

    eng_personal = relationship('EngineerPersonal', back_populates='workshop')
    product_category = relationship('ProductCategory', back_populates='workshop')

class TestLaboratories(Base):
    '''Таблица описывающая лаборатории'''

    __tablename__ = 'test_laboratories'

    id: Mapped[intpk]
    name: Mapped[str]
    test_date_start: Mapped[datetime] = mapped_column(DateTime, server_default=text("NOW()"))
    test_date_finish: Mapped[str | None]

    products = relationship('Product', back_populates='laboratory')
    personal_lab = relationship('PersonalLaboratories', back_populates='laboratory')
    tools = relationship('Tools', back_populates='laboratory')

class PersonalLaboratories(Base):
    '''Таблица описывающая персонал лабораторий'''

    __tablename__ = 'personal_laboratories'

    id: Mapped[intpk] 
    full_name: Mapped[str]
    birthday: Mapped[str]
    status: Mapped[str]
    laboratory_id: Mapped[int] = mapped_column(ForeignKey('test_laboratories.id'))

    laboratory = relationship('TestLaboratories', back_populates='personal_lab')

class Tools(Base):
    '''Таблица описывающая инструменты для лабораторий'''

    __tablename__ = 'tools'

    id: Mapped[intpk]
    name: Mapped[str]
    laboratory_id: Mapped[int] = mapped_column(ForeignKey('test_laboratories.id', ondelete="CASCADE"))

    laboratory = relationship('TestLaboratories', back_populates='tools')

class WorksWithProduct(Base):
    '''Таблица описывающая работы с продуктом'''

    __tablename__ = 'works_with_product'

    id: Mapped[intpk]
    name: Mapped[str]
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete="CASCADE"))

    product = relationship('Product', back_populates='works_for_product')