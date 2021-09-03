from .auth import get_password_hash, verify_password, create_access_token
from .models import User
from fastapi import HTTPException, status

def login_service(auth_details, db):
    auth_details.username = auth_details.username.strip()
    user = db.query(User).filter(User.username == auth_details.username).first()
    if user is None or not verify_password(auth_details.password, user.password):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    data={'id': user.id}
    token = create_access_token(data, expire_minutes=30)
    return {'token': token}

def register_service(auth_details, db):
    auth_details.username = auth_details.username.strip()
    is_username_is_taken = db.query(User).filter(User.username == auth_details.username).first()
    if is_username_is_taken:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is taken")
    if len(auth_details.username) < 4:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username must be at least 4 chars")
    if len(auth_details.password) < 8:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 chars")
    
    hashed_password = get_password_hash(auth_details.password)
    auth_details.password = hashed_password
    user = User(**auth_details.dict())
    db.add(user)
    db.commit()
    db.refresh(user)

    data={'id': user.id}
    token = create_access_token(data, expire_minutes=30)
    return {'token': token}

def get_user_by_id(id, db):
    return db.query(User).filter_by(id=id).first()
