from fastapi import APIRouter, Depends, HTTPException, status, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from . import auth, services
from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

router, templates = APIRouter(prefix='/admin', tags=['Admin']), Jinja2Templates(directory="./templates")

@router.get('/login', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
    
@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get('/category/add', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("add_category.html", {"request": request})

@router.get('/image/add', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("add_image.html", {"request": request})

@router.get('/category/{cat_id}', response_class=HTMLResponse)
async def category(request: Request, cat_id: int):
    return templates.TemplateResponse("category.html", {"request": request, 'cat_id': cat_id})

@router.post('/api/login')
async def api_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = await auth.authencticate_admin(username=form_data.username, password=form_data.password)
    if user_dict:
        return {'success': True, 'token': await auth.create_access_token(user_dict=user_dict, expiry_time_duration=timedelta(minutes=3000))}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='username or password invalid.')

@router.get('/api/category')
async def api_get_all_category(page_no: int, user_dict: auth.verify_token_dep) -> dict:
    return await services.get_all_categories(page_no=page_no)

@router.get('/api/search/category')
async def api_get_all_category(search: str|None, user_dict: auth.verify_token_dep) -> dict:
    return await services.get_all_categories(search=search, page_no=None)

@router.post('/api/category/add')
async def api_add_category(user_dict: auth.verify_token_dep, cat_name: Annotated[str, Form()], cat_sub_title: Annotated[str, Form()], cat_is_active: Annotated[bool, Form()], cat_cover_image: Annotated[UploadFile, File(media_type="image/png, image/jpeg, image/jpg")]) -> dict:
    if cat_cover_image.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
        return {'success': True, 'msg': 'file type must be image/png or image/jpeg'}
    return await services.add_category(cat_name=cat_name, cat_cover_image=cat_cover_image, cat_is_active=cat_is_active, cat_sub_title=cat_sub_title)

@router.get('/api/category/{cat_id}')
async def api_get_category(cat_id: int, user_dict: auth.verify_token_dep) -> dict:
    return await services.get_category(cat_id=cat_id)

@router.get('/api/category/{cat_id}/images')
async def api_get_category_images(cat_id: int, page_no: int, user_dict: auth.verify_token_dep) -> dict:
    return await services.get_category_images(cat_id=cat_id, page_no=page_no)

@router.get('/api/image/{img_id}')
async def api_get_image(img_id: int, user_dict: auth.verify_token_dep) -> dict:
    return await services.get_image(img_id=img_id)
