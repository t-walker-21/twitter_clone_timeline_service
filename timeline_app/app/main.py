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
    statement = select(Follower.followee_id).where(Follower.follower_id == current_user['sub'])
    people_followed = session.exec(statement).all()
    people_followed_str = [str(person) for person in people_followed]
        
    #print (people_followed)

    tweets = []
    #for followee in people_followed:
        #print (f"searching for tweets for {followee}")
    for tweet in TweetDocument.objects(user_id__in=people_followed_str):
        tweets.append(json.loads(tweet.to_json()))

    #TODO: Move this to the DB call
    tweets.sort(key=lambda x: x['created_at']['$date'], reverse=True)
        
    return {'tweets': tweets}
