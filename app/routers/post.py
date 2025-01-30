from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db


async def find_post(id: int, db: Session):
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found"
        )
    return post


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("/", response_model=list[schemas.PostOut])  # ,
async def read_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = None,
):
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search) if search else text(""))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [{"Post": post, "Votes": votes} for post, votes in results]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
async def read_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = await find_post(int(id), db)
    return {"Post": post[0], "Votes": post[1]}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = await find_post(int(id), db)
    if post[0].owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to Perform this Action",
        )
    db.delete(post[0])
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == int(id))
    db_post = post_query.first()
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found"
        )
    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to Perform this Action",
        )
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
