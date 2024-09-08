import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

Base = declarative_base()
engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)

class UserSession(Base):
    __tablename__ = 'user_sessions'
    id = Column(Integer, primary_key=True)
    session_id = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Float)
    ip_address = Column(String)
    user_agent = Column(String)

class UserAction(Base):
    __tablename__ = 'user_actions'
    id = Column(Integer, primary_key=True)
    session_id = Column(String)
    timestamp = Column(DateTime)
    action_type = Column(String)
    prompt = Column(String)
    prompt_length = Column(Integer)
    response = Column(String)  # New column
    response_length = Column(Integer)
    response_time = Column(Float)

class APICall(Base):
    __tablename__ = 'api_calls'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    endpoint = Column(String)
    request_payload = Column(String)
    response_status = Column(Integer)
    response_time = Column(Float)

class ErrorLog(Base):
    __tablename__ = 'error_logs'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    error_type = Column(String)
    error_message = Column(String)
    stack_trace = Column(String)
    session_id = Column(String)

Base.metadata.create_all(engine)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
