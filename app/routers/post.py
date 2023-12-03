from fastapi import Body, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2
from typing import List,Optional
from sqlalchemy import func
router = APIRouter(
    prefix="/Posts",
    tags=["posts"]
)

@router.get('/', response_model=List[schemas.PostView])
def get_posts(db: Session = Depends(get_db),limit:int=10,skip:int=0,search:Optional[str]=""):
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()
    return results

@router.get('/myposts', response_model=List[schemas.PostOut])
def get_my_posts(db: Session = Depends(get_db),current_user:dict=Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.owner_name==current_user.username).all()
    return posts

@router.get('/{id}', response_model=schemas.PostView)
def get_post(id: int, db: Session = Depends(get_db),current_user:dict=Depends(oauth2.get_current_user)):
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@router.post('/', response_model=schemas.PostCreateOut, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user:dict  = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())  # Create a new Post instance with data from the request
    new_post.owner_name=current_user.username
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user:dict = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    post_=post.first()
    if post_.owner_name!=current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to do this operation")
    if post.first():
        post.delete(synchronize_session=False)
        db.commit()
        return {"detail": "Post deleted"}

    raise HTTPException(status_code=404, detail="No post with the given id")

@router.put("/{id}", response_model=schemas.PostOut)
def update_post(id: int, new_post: schemas.PostUpdate, db: Session = Depends(get_db),current_user:dict  = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post.owner_name!=current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to do this operation")
    if post:
        for field, value in new_post.dict().items():
            setattr(post, field, value)
        db.commit()
        db.refresh(post)
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post with the given id")
