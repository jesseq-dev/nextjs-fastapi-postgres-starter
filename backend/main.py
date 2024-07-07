from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select
from datetime import datetime
from seed import seed_user_if_needed, seed_threads_if_needed
from sqlalchemy.ext.asyncio import AsyncSession
from db_engine import engine
from models import User, Thread, Message
from randomdata import generate_random_sentence

seed_user_if_needed()
seed_threads_if_needed()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRead(BaseModel):
    id: int
    name: str

class ThreadRead(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class MessageCreate(BaseModel):
    thread_id: int
    content: str
    sender_id: int

class MessageRead(BaseModel):
    id: int
    thread_id: int
    content: str
    sender_id: int | None
    created_at: datetime

async def get_user():
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Sample logic to simplify getting the current user. There's only one user.
            result = await session.execute(select(User))
            user = result.scalars().first()

            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return UserRead(id=user.id, name=user.name)
        
@app.get("/users/me", response_model=UserRead)
async def get_my_user():
    return await get_user()

@app.get("/threads", response_model=list[ThreadRead])
async def get_user_threads(user: UserRead = Depends(get_my_user)):
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(Thread).filter_by(user_id=user.id))
            threads = result.scalars().all()
            if not threads:
                raise HTTPException(status_code=404, detail="No threads found")
            return [
                ThreadRead(id=thread.id, user_id=thread.user_id, created_at=thread.created_at, updated_at=thread.updated_at)
                for thread in threads
            ]
        
@app.post("/threads/")
async def create_thread(user: UserRead = Depends(get_my_user)):
    async with AsyncSession(engine) as session:
        async with session.begin():            
            new_thread = Thread(user_id=user.id)
            session.add(new_thread)
            await session.commit()
            await session.refresh(new_thread)
            return ThreadRead(id=new_thread.id, user_id=new_thread.user_id, created_at=new_thread.created_at, updated_at=new_thread.updated_at)
        
@app.get("/threads/{thread_id}", response_model=ThreadRead)
async def get_thread(thread_id: int):
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(Thread).filter_by(id=thread_id))
            thread = result.scalars().first()
            if thread is None:
                raise HTTPException(status_code=404, detail="Thread not found")
            return ThreadRead(id=thread.id, user_id=thread.user_id, created_at=thread.created_at, updated_at=thread.updated_at)

@app.post("/thread/messages/", response_model=list[MessageRead])
async def create_message(message_create: MessageCreate):
    async with AsyncSession(engine) as session:
        async with session.begin():
            result_thread = await session.execute(select(Thread).filter_by(id=message_create.thread_id))
            thread = result_thread.scalars().first()
            if thread is None:
                raise HTTPException(status_code=404, detail="Thread not found")

            new_message = Message(
                thread_id=message_create.thread_id,
                content=message_create.content,
                sender_id=message_create.sender_id
            )
            session.add(new_message)
            await session.flush()
            await session.refresh(new_message)

            bot_content = generate_random_sentence()
            bot_message = Message(content=bot_content, sender_id=None, thread_id=message_create.thread_id)
            session.add(bot_message)
            await session.flush()
            await session.refresh(bot_message)
            
            print("ssssss")
            return [MessageRead(
                id=new_message.id,
                thread_id=new_message.thread_id,
                content=new_message.content,
                sender_id=new_message.sender_id,
                created_at=new_message.created_at
            ), MessageRead(
                id=bot_message.id,
                thread_id=bot_message.thread_id,
                content=bot_message.content,
                sender_id=bot_message.sender_id,
                created_at=bot_message.created_at
            )]
        
@app.get("/threads/{thread_id}/messages", response_model=list[MessageRead])
async def get_messages(thread_id: int):
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(Message).filter_by(thread_id=thread_id).order_by(Message.created_at))
            messages = result.scalars().all()
            return [MessageRead(
                id=msg.id,
                thread_id=msg.thread_id,
                content=msg.content,
                sender_id=msg.sender_id,
                created_at=msg.created_at
            ) for msg in messages]
        
