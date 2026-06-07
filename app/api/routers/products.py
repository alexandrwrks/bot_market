from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from app.api.config_template import templates
from app.api.service.products import products_service

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/", name="products_page", response_class=HTMLResponse)
async def get_products(request: Request):
    products = await products_service.get_all_products()
    return templates.TemplateResponse(
        name="products.html", request=request, context={"products": products}
    )
