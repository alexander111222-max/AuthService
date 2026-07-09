
from fastapi import APIRouter, Depends
from src.api.dependencies import check_permission
from src.models.permissions import ActionEnum
import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mock", tags=["Mock - Бизнес объекты"])

MOCK_PRODUCTS = [
    {"id": 1, "name": "Ноутбук", "price": 999, "owner_id": 1},
    {"id": 2, "name": "Телефон", "price": 499, "owner_id": 2},
    {"id": 3, "name": "Планшет", "price": 299, "owner_id": 1},
]

MOCK_ORDERS = [
    {"id": 1, "product_id": 1, "status": "pending", "owner_id": 1},
    {"id": 2, "product_id": 2, "status": "completed", "owner_id": 2},
    {"id": 3, "product_id": 3, "status": "cancelled", "owner_id": 1},
]

MOCK_SHOPS = [
    {"id": 1, "name": "Магазин на главной", "city": "Москва", "owner_id": 1},
    {"id": 2, "name": "Онлайн магазин", "city": "СПб", "owner_id": 2},
]


@router.get(
    "/products",
    summary="Получить все товары",
    description="Доступно всем авторизованным пользователям с правом read на products.",
    dependencies=[Depends(check_permission("products", ActionEnum.read))],
)
async def get_products():
    logger.info("Запрос списка товаров")
    return MOCK_PRODUCTS


@router.post(
    "/products",
    summary="Создать товар",
    description="Доступно менеджерам и администраторам",
    dependencies=[Depends(check_permission("products", ActionEnum.create))],
)
async def create_product():
    logger.info("Создание нового товара")
    return {"id": 4, "name": "Новый товар", "price": 199, "owner_id": 1}


@router.patch(
    "/products/{product_id}",
    summary="Обновить товар",
    description="Менеджер может обновлять только свои товары, админ - любые",
    dependencies=[Depends(check_permission("products", ActionEnum.update))],
)
async def update_product(product_id: int):
    logger.info(f"Обновление товара с id: {product_id}")
    return {"id": product_id, "name": "Обновлённый товар", "price": 399, "owner_id": 1}


@router.delete(
    "/products/{product_id}",
    summary="Удалить товар",
    description="Доступно только администраторам",
    dependencies=[Depends(check_permission("products", ActionEnum.delete))],
)
async def delete_product(product_id: int):
    logger.info(f"Удаление товара с id: {product_id}")
    return {"status": "ok", "deleted_id": product_id}


@router.get(
    "/orders",
    summary="Получить все заказы",
    description="Доступно всем авторизованным пользователям с правом read",
    dependencies=[Depends(check_permission("orders", ActionEnum.read))],
)
async def get_orders():
    logger.info("Запрос списка заказов")
    return MOCK_ORDERS


@router.post(
    "/orders",
    summary="Создать заказ",
    description="Доступно менеджерам и администраторам",
    dependencies=[Depends(check_permission("orders", ActionEnum.create))],
)
async def create_order():
    logger.info("Создание нового заказа")
    return {"id": 4, "product_id": 1, "status": "pending", "owner_id": 1}


@router.patch(
    "/orders/{order_id}",
    summary="Обновить заказ",
    description="Менеджер может обновлять только свои заказы, админ - любые",
    dependencies=[Depends(check_permission("orders", ActionEnum.update))],
)
async def update_order(order_id: int):
    logger.info(f"Обновление заказа с id: {order_id}")
    return {"id": order_id, "status": "completed"}


@router.delete(
    "/orders/{order_id}",
    summary="Удалить заказ",
    description="Доступно только администраторам",
    dependencies=[Depends(check_permission("orders", ActionEnum.delete))],
)
async def delete_order(order_id: int):
    logger.info(f"Удаление заказа с id: {order_id}")
    return {"status": "ok", "deleted_id": order_id}


@router.get(
    "/shops",
    summary="Получить все магазины",
    description="Доступно всем авторизованным пользователям с правом read",
    dependencies=[Depends(check_permission("shops", ActionEnum.read))],
)
async def get_shops():
    logger.info("Запрос списка магазинов")
    return MOCK_SHOPS


@router.post(
    "/shops",
    summary="Создать магазин",
    description="Доступно менеджерам и администраторам",
    dependencies=[Depends(check_permission("shops", ActionEnum.create))],
)
async def create_shop():
    logger.info("Создание нового магазина")
    return {"id": 3, "name": "Новый магазин", "city": "Казань", "owner_id": 1}


@router.patch(
    "/shops/{shop_id}",
    summary="Обновить магазин",
    description="Менеджер может обновлять только свои магазины, админ - любые",
    dependencies=[Depends(check_permission("shops", ActionEnum.update))],
)
async def update_shop(shop_id: int):
    logger.info(f"Обновление магазина с id: {shop_id}")
    return {"id": shop_id, "name": "Обновлённый магазин", "city": "Казань"}


@router.delete(
    "/shops/{shop_id}",
    summary="Удалить магазин",
    description="Доступно только администраторам",
    dependencies=[Depends(check_permission("shops", ActionEnum.delete))],
)
async def delete_shop(shop_id: int):
    logger.info(f"Удаление магазина с id: {shop_id}")
    return {"status": "ok", "deleted_id": shop_id}