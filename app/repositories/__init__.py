from app.repositories.category_repository import (
    create_category,
    get_category_by_id,
    get_category_by_name,
    get_categories,
    update_category,
    delete_category,
)

from app.repositories.product_repository import (
    create_product,
    get_product_by_id,
    get_products,
    get_products_by_category,
    update_product,
    delete_product,
)