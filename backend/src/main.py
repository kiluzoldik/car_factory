from fastapi import FastAPI

from .router import product_router, product_category_router, personal_category_router, \
    engineer_personal_router, personal_workers_router, brigades_router, workshops_router, \
    laboratories_router, personal_laboratories_router, tools_router, works_with_product_router


app = FastAPI(
    title='Car Factory',
)

app.include_router(product_router)

app.include_router(product_category_router)

app.include_router(personal_category_router)

app.include_router(engineer_personal_router)

app.include_router(personal_workers_router)

app.include_router(brigades_router)

app.include_router(workshops_router)

app.include_router(laboratories_router)

app.include_router(personal_laboratories_router)

app.include_router(tools_router)

app.include_router(works_with_product_router)
