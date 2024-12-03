from mongoengine import Document, connect
from mongoengine.fields import StringField, ListField, DateTimeField, BooleanField
from datetime import datetime
import os

connect(host=os.environ.get("MONGODB_URI_STRING", "mongodb://localhost:27017/tweets"))

class TweetDocument(Document):
    tweet_content = StringField(required=True, max_length=200)
    username = StringField(required=True)
    user_id = StringField(required=True)
    likes = ListField(field=user_id)
    mentions = ListField(field=user_id)
    hashtags = ListField(field=StringField())
    created_at = DateTimeField(default=datetime.now)
    is_edited = BooleanField(default=False)