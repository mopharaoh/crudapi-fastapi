from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import post,user,auth,vote
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# before db use array
# def findPost(id):
#     for i in posts:
#         if i['id']==id:
#             return i

# def find_index_post(id):
#     for i,p in enumerate(posts):
#         if p['id']==id:
#             return i

