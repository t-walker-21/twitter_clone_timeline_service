# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from db.sql.db_connection import get_session
from db.sql.models import Follower
from db.mongo.models import TweetDocument
import jwt
import json

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    
    if token is None:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user_info = jwt.decode(jwt=token, key="secret", algorithms=["HS256",])
    return user_info  # In a real application, you would return a user object

@app.get("/timeline/")
def generate_timeline(session: Session = Depends(get_session), current_user: str = Depends(get_current_user)):

    #print (f"current user: {current_user['sub']}")
    statement = select(Follower).where(Follower.follower_id == current_user['sub'])
    results = session.exec(statement)
    people_followed = []
    for result in results:
        people_followed.append(str(result.followee_id))
        
    #print (response)

    tweets = []
    for followee in people_followed:
        for tweet in TweetDocument.objects(user_id=followee):
        
            tweets.append(json.loads(tweet.to_json()))
        
    return {'tweets': tweets}