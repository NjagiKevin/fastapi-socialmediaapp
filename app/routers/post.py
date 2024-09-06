from multiprocessing.sharedctypes import synchronized
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func #gives us access to fnxs like Count

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# getting all posts
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10, 
    skip: int = 0, 
    search: Optional[str] = ""
):
    # Query for posts and their vote counts
    results = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(
        models.Post.id
    ).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).all()

    # Format the results to include vote counts in the response
    response = []
    for post, votes in results:
        # Convert SQLAlchemy model to Pydantic schema
        post_data = schemas.Post.from_orm(post)  # Convert to Pydantic model
        response.append({"Post": post_data, "votes": votes})

    return response


# creating a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session=Depends(get_db),
                 current_user: int = Depends (oauth2.get_current_user)): # if a resource requires one to be logged in, we expect them to provide an access token
    new_post=models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post) #adding to db
    db.commit()
    db.refresh(new_post)#to return newly added
    return new_post


# getting a single post
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, db: Session=Depends(get_db),
             current_user: int = Depends (oauth2.get_current_user)):
    #post=db.query(models.Post).filter(models.Post.id==id).first()

    post= db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(
        models.Post.id
    ).filter(
        models.Post.id==id
    ).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    # Check if the logged-in user is the owner of the post
    #if post.owner_id != current_user.id:
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            #detail="Not authorized to perform the requested action")
    return post


# deleting a post
@router.delete("/{id}")
def deleted_post(id: int, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # Fetch the post to be deleted
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()  # Correct: Getting the first post here

    # Check if post exists
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    # Check if the logged-in user is the owner of the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform the requested action")
    
    # Delete the post
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




# updating a post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: dict = Depends(oauth2.get_current_user)):  # Correct here

    # Retrieve the post to update
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # Check if the post exists
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    # Ensure the current user is the owner of the post
    if post.owner_id != current_user.id:  # Correct here
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform the requested action")

    # Update the post
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    # Return the updated post
    return post_query.first()

