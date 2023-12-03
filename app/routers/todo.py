from fastapi import Body,APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..database import get_db
from ..import schemas,models,oauth2
from typing import List

router=APIRouter(
    prefix="/Tasks",
    tags=["Tasks"]
)

@router.get("/",response_model=List[schemas.TaskOut])
def get_task(db: Session=Depends(get_db),current_user: dict = Depends(oauth2.get_current_user)):
    Task=db.query(models.Task).all()
    return Task


@router.get("/{id}",response_model=schemas.TaskOut)
def get_task_id(id: int,db:Session=Depends(get_db),current_user:dict=Depends(oauth2.get_current_user)):
    task=db.query(models.Task).filter(models.Task.id==id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found")
    
    return task


@router.post("/",response_model=schemas.TaskOut)
def add_task(task: schemas.TaskBase,db:Session=Depends(get_db),current_user:dict=Depends(oauth2.get_current_user)):
    new_task=models.Task(**task.dict())
    new_task.owner_name=current_user.username
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int ,db:Session=Depends(get_db),current_user:dict=Depends(oauth2.get_current_user)):
    task=db.query(models.Task).filter(models.Task.id==id)
    
    if task.first():
        task_first=task.first()
        if task_first.owner_name!=current_user.username:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized operation")
        task.delete(synchronize_session=False)
        db.commit()
        return {"detail": "Task deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task Not found")
   

@router.put("/{id}",response_model=schemas.TaskOut)
def update_post(id:int,new_task: schemas.TaskBase,db:Session=Depends(get_db),current_user:dict=Depends(oauth2.get_current_user)):
    task=db.query(models.Task).filter(models.Task.id==id).first()
    task_=task.firt()

       
   
    if task:
        if task_.owner_name!=current_user.username:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden no operation")
        for field, value in new_task.dict().items():
            setattr(task, field, value)
        db.commit()
        db.refresh(task)
        return task
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post with the given id")

    