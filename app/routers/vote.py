from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter 
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from typing import List


router=APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session=Depends(database.get_db), 
         current_user: int=Depends(oauth2.get_current_user)):
    
    #logic to detect if a user if voting on a post that doesnt exist
    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.post_id} does not exist")

    #checks if this specific user has already voted for this post
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, 
                                            models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()

    if (vote.dir==1):
        #does vote already exist?
        if found_vote:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"user {current_user.id} has already voted on post {vote.post_id}")

        
        #if we didnt find a vote, we create a new vote
        new_vote=models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully created vote"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exist")
        
        # if we found a vote, we have to delete it
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}

        