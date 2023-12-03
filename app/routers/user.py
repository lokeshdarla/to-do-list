from fastapi import Body,APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..database import get_db
from ..import schemas,models,oauth2
from typing import List
from ..import utils

router=APIRouter(
    prefix="/Users",
    tags=["Users"]
)

@router.get("/",response_model=List[schemas.UserOut])
def get_user(db: Session=Depends(get_db)):
    users=db.query(models.User)
    return users

@router.get("/{id}",response_model=schemas.UserOut)
def get_user_id(id: int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    return user


@router.post("/")
def add_user(user: schemas.UserCreate,db:Session=Depends(get_db)):
    user.password=utils.hash(user.password)
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"detail":"Signup Successful"}


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int ,db:Session=Depends(get_db),username:str=Depends(oauth2.get_current_user)):
    user=db.query(models.User).filter(models.User.id==id)
    if user.first():
        user.delete(synchronize_session=False)
        db.commit()
        return {"detail": "user removed"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not found")
   

@router.put("/{id}",response_model=schemas.UserOut)
def update_post(id:int,new_user: schemas.UserUpdate,db:Session=Depends(get_db),username:str=Depends(oauth2.get_current_user)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if user:
        for field, value in new_user.dict().items():
            setattr(user, field, value)
        db.commit()
        db.refresh(user)
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post with the given id")
