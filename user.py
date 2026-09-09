from fastapi import FastAPI
import uvicorn

app=FastAPI()
user_db = [(1, "john", "john@gmail.com"),(2, "jay", "jay@outlook.com"),(3, "priya", "priya123@gmail.com")]
@app.get("/")
def users():
    return user_db
@app.get("/users/new")
def new_user(user_id:int,name:str,email:str):
    user_db.append((user_id,name,email))
    return user_db

@app.get("/users/{user_id}")
def user(user_id: int):
    for items in user_db:
        if items[0] == user_id:
            return {"User Details": items}
    return {"error": "User id not defined"}

if __name__=="__user__":
    uvicorn.run(app,host="localhost",port=8001)