from fastapi import APIRouter, Depends, HTTPException, status

from .schemas import AuthSchema, UserInfo
from database_init import get_db
from sqlalchemy.orm import Session
from .services import register_service, login_service, get_user_by_id
from .auth import get_current_user

router = APIRouter(prefix="/user", tags=["User"])

@router.post('/login')
def login(auth_details: AuthSchema, db: Session = Depends(get_db)):
    response = login_service(auth_details, db)
    if HTTPException is type(response):
        raise response
    return response

@router.post('/register')
def register(auth_details: AuthSchema, db: Session = Depends(get_db)):
    response = register_service(auth_details, db)
    if HTTPException is type(response):
        raise response
    return response

@router.get('', status_code=status.HTTP_200_OK)
def get_user_info(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    data = get_user_by_id(current_user.get('id'), db)
    return UserInfo.from_orm(data)