from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
    prefix="/votes",
    tags=["Votes"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {vote.post_id} not found",
        )
    current_vote = (
        db.query(models.Vote)
        .filter(
            models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
        )
        .first()
    )
    if vote.dir == 1:
        if current_vote is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} already voted on post {vote.post_id}",
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return new_vote
    else:
        if current_vote is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {current_user.id} has not voted on post {vote.post_id}",
            )
        db.delete(current_vote)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
