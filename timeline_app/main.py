# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from db.db_connection import get_session
from db.models import User, Follower
from datetime import datetime
import jwt

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    
    if token is None:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user_info = jwt.decode(jwt=token, key="secret", algorithms=["HS256",])
    return user_info  # In a real application, you would return a user object

@app.get("/timeline/")
def get_followers(session: Session = Depends(get_session), current_user: str = Depends(get_current_user)):

    statement = select(Follower).where(Follower.followee_id == user_id)
    results = session.exec(statement)
    response = []
    for result in results:
        response.append({'id': result.id,
                         'follower_id': result.follower_id,
                         'followee_id': result.followee_id})
        
    return {'users': response}