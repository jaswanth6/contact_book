from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
import mysql.connector

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Replace the placeholders with  MySQL database credentials
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="contact_book"
)
def get_cursor():
    return db.cursor()

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("new.html", {"request": request})

@app.post("/")
def add_contact(
    request: Request,
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    relation: str = Form(...)
):
    cursor = get_cursor()
    cursor.execute(
        "INSERT INTO contacts (name, phone, email, relation) VALUES (%s, %s, %s, %s)",
        (name, phone, email, relation)
    )
    db.commit()
    return templates.TemplateResponse("new.html", {"request": request, "success": True})

@app.get("/contacts")
def contacts(request: Request):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    return templates.TemplateResponse("mkdir.html", {"request": request, "contacts": contacts})

import uvicorn

uvicorn.run(app)