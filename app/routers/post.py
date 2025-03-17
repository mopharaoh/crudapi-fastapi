from .. import models,schemas,oauth2
from fastapi import Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List,Optional

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session=Depends(get_db),
              current_user:int=Depends(oauth2.get_current_user),
              limit:int=10,search:Optional[str]=""):
    # return db.query(models.Post).all()
    # # cursor.execute("""SELECT * FROM posts """)
    # # postss=cursor.fetchall()
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()

    # results=
    # print(results)
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def createpost(post: schemas.PostCreate,db: Session=Depends(get_db),
               current_user:int=Depends(oauth2.get_current_user)):
    # use orm
    
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # use sql commands
    # cursor.execute("""insert into posts (title, content, published) values (%s,%s,%s) returning * """,
    #                         (post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    # use native
    # post_dict=post.dict()
    # post_dict['id']=randrange(0,1000000)
    # posts.append(post_dict)

    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def read(id: int,response: Response,db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    # post=findPost(id)
    # cursor.execute("""select * from posts where id = %s """,(str(id),))
    # post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
        
        # response.status_code=404
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'message':f"post with id : {id} was not found "}
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int,db: Session=Depends(get_db),
           current_user:int=Depends(oauth2.get_current_user)):
    
    del_post=db.query(models.Post).filter(models.Post.id==id)
    # ind=find_index_post(id)
    # cursor.execute("""delete from posts where id = %s returning *""",(str(id),))
    # del_post=cursor.fetchone()
    # conn.commit()
    if del_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
    
    if del_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    del_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def updatePost(id: int,post: schemas.PostCreate,db: Session=Depends(get_db),
               current_user:int=Depends(oauth2.get_current_user)):
    updatedpost=db.query(models.Post).filter(models.Post.id==id)
    
    # ind=find_index_post(id)
    # cursor.execute("""update posts set title = %s, content= %s, published= %s where id = %s returning * """,
    #                (post.title,post.content,post.published,(str(id))))
    # updated_Post=cursor.fetchone()
    # conn.commit()
    if updatedpost.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
    
    if updatedpost.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    

    updatedpost.update(post.dict(),synchronize_session=False)
    db.commit()
    # post_dict=post.dict()
    # post_dict['id']=id
    # posts[ind]=post_dict
    return updatedpost.first()
