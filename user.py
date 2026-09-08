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

books = [
{"id": 1, "title": "Python Basics", "author": "Guido"},
{"id": 2, "title": "FastAPI Deep Dive", "author": "Tiangolo"},
]

@app.get("/book/{book_id}")
def book_search(book_id:int):
    for book in books:
        if book["id"]==book_id:
            return book
@app.get("/search")
def author_name(author:str):
    for book in books:
        if book["author"]==author:
            return book
        else:
            return "Not Found"



if __name__=="__user__":
    uvicorn.run(app,host="localhost",port=8001)