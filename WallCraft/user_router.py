from fastapi import APIRouter, Depends
from . import auth, services

router = APIRouter(prefix='/user', tags=['User'])


@router.get('/category')
async def get_all_category(page_no: int, username: str = Depends(auth.basic_authentication)) -> dict:
    return await services.get_all_categories(page_no=page_no)


@router.get('/category/{cat_id}')
async def get_category(cat_id: int, username: str = Depends(auth.basic_authentication)) -> dict:
    return await services.get_category(cat_id=cat_id)


@router.get('/category/{cat_id}/images')
async def get_category_images(cat_id: int, page_no: int, username: str = Depends(auth.basic_authentication)) -> dict:
    return await services.get_category_images(cat_id=cat_id, page_no=page_no)


@router.get('/image/{img_id}')
async def get_image(img_id: int, username: str = Depends(auth.basic_authentication)) -> dict:
    return await services.get_image(img_id=img_id)
