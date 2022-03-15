from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from pydantic import BaseModel
from random import randrange
from passlib.context import CryptContext
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from . database import engine, get_db
from sqlalchemy.orm import Session
from . routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True

while True:

    try: 
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='balaji123',
        cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database was successfully connected")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)   
        time.sleep(5) 

my_posts = [{"Title" : "Post 1", "Content" : "This is my 1st post", "id": 1}, 
{"Title" : "Post 2", "Content" : "I like to play Soccer", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"Message": "Hello World"}

