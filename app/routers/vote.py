from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session
from .. import schemas,database,oauth2,models

router=APIRouter(
    prefix="/Vote",
    tags=["Vote"]
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def upvote(vote:schemas.Vote,db:Session=Depends(database.get_db),current_user:dict  = Depends(oauth2.get_current_user)):
    
    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_name==current_user.username)
    found_vote=vote_query.first()
    if(vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Already Liked")
        new_vote=models.Vote(post_id=vote.post_id,user_name=current_user.username)
        db.add(new_vote)
        db.commit()
        return{"message": "Successfully added vote"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="You have not liked the post")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"Successfully deleted vote"}