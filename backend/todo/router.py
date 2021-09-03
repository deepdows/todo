from fastapi import APIRouter, status, Depends, Response

from database_init import get_db

from user.auth import get_current_user
from sqlalchemy.orm import Session
from .schemas import TodoCreate, TodoShow, TodoUpdate, TodoShow
from .services import create_task_service, get_tasks_service_of_user, delete_task_by_id, update_task_by_id
from typing import List

router = APIRouter(prefix="/todo", tags=["Todo"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(request: TodoCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    response = create_task_service(request, db, current_user.get('id'))
    return TodoShow.from_orm(response)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[TodoShow])
async def get_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    response = get_tasks_service_of_user(current_user.get('id'), db)
    return response

@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_task(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    delete_task_by_id(id, db, current_user.get('id'))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_task(id: int, request: TodoUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    response = update_task_by_id(request, id, current_user.get('id'), db)
    return TodoShow.from_orm(response)