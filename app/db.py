from sqlalchemy import Column, BigInteger, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TweetSent(Base):
    __tablename__ = "tweets_sent"

    id = Column(BigInteger, primary_key=True)
    message_id = Column(BigInteger)
    tweet_time = Column(Integer)
    author_handle = Column(String(100))
