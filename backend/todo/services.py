from fastapi import HTTPException, status
from .models import Todo

def create_task_service(data, db, user_id):
    data.title = data.title.strip()
    if len(data.title) < 1:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Title is too small')
    if len(data.title) > 100:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Title is more than 100 chars')
    new_task = Todo(**data.dict(), user_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks_service_of_user(user_id, db):
    tasks = db.query(Todo).filter_by(user_id=user_id).order_by(Todo.created_date.desc()).all()
    return tasks

def delete_task_by_id(id, db, user_id):
    task = db.query(Todo).filter(Todo.user_id==user_id, Todo.id==id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    db.delete(task)
    db.commit()

def update_task_by_id(data, id, user_id, db):
    task = db.query(Todo).filter(Todo.user_id==user_id, Todo.id==id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    if data.title:
        data.title = data.title.strip()
        if len(data.title) < 1:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Title is too small')
        if len(data.title) > 100:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Title is more than 100 chars')
    for attr, value in data.dict().items():
        if value is not None:
            setattr(task, attr, value)
    db.commit()
    db.refresh(task)

    return task