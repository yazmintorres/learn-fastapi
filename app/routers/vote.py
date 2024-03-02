from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, oauth2, models

router = APIRouter(prefix="/vote", tags=["Votes"])

@router.post("", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # check that post exists 
    post = db.query(models.Post).filter_by(id = vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post {vote.post_id} does not exist")

    # check if the vote exists or not 
    existing_vote = db.query(models.Vote).filter_by(post_id = vote.post_id, user_id = current_user.id).first()
    if (vote.dir == 1):
        if existing_vote:
            # if vote already exists, raise exception 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User {current_user.id} has already voted on post {vote.post_id} ")
       
        # add to vote table
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
        
    else:
        if existing_vote: 
            db.delete(existing_vote)
            db.commit()
            return {"message": "successfully deleted vote"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Vote does not exist for post {vote.post_id} and user {current_user.id}")