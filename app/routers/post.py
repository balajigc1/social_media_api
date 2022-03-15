from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db
from typing import Optional, List

router = APIRouter(tags=['Posts'])

@router.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):       

    posts = db.query(models.Post).all()    
    return posts

# @router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
#     # cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * """, (post.title, post.content))
#     # new_post = cursor.fetchone()
#     # conn.commit() 

#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return new_post

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * """, (post.title, post.content))
    # new_post = cursor.fetchone()
    # conn.commit() 

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} not found')    
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING * """, (post.title, post.content, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    
    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()